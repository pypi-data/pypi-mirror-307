import fast_vertex_quality_inference.tools.globals as myGlobals
import onnxruntime as ort
import pandas as pd
import numpy as np
import pickle


def apply_correction_to_gaussian(nominal_vertexing_output, Transformers):

    update_nominal = True

    alt_vertexing_output = nominal_vertexing_output.copy()

    targets = list(nominal_vertexing_output.keys())
    targets = [
        target
        for target in targets
        if "DIRA" not in target and "VTXISOBDT" not in target
    ]

    with open(f"{myGlobals.SYST_MODELS_PATH}gaussian_maps.pkl", "rb") as f:
        maps = pickle.load(f)

    for target in targets:
        gen_variable_sorted, gen_variable_gaussian_sorted = maps[target]
        pp_MOTHER_ENDVERTEX_CHI2 = Transformers[target].process(
            np.asarray(nominal_vertexing_output[target])
        )
        pp_MOTHER_ENDVERTEX_CHI2_prime = np.interp(
            pp_MOTHER_ENDVERTEX_CHI2, gen_variable_sorted, gen_variable_gaussian_sorted
        )
        nominal_vertexing_output[target] = Transformers[target].unprocess(
            pp_MOTHER_ENDVERTEX_CHI2_prime
        )

    if update_nominal:
        return nominal_vertexing_output, alt_vertexing_output
    else:
        return alt_vertexing_output, nominal_vertexing_output


def get_eta_weight(data_tuple):

    with open(f"{myGlobals.SYST_MODELS_PATH}eta_weighting_info.pkl", "rb") as handle:
        weight_info = pickle.load(handle)

    bin_edges = weight_info["bin_edges"]
    ratio = weight_info["ratio"]

    weight = np.ones(np.shape(data_tuple.tuple["DAUGHTER1_eta"]))

    for particle in ["DAUGHTER1", "DAUGHTER2", "DAUGHTER3"]:

        for bindx in range(len(bin_edges) - 1):

            lower_edge = bin_edges[bindx]
            upper_edge = bin_edges[bindx + 1]

            weight_factor = ratio[bindx]

            within_bin = (data_tuple.tuple[f"{particle}_eta"] >= lower_edge) & (
                data_tuple.tuple[f"{particle}_eta"] < upper_edge
            )
            weight[
                within_bin
            ] *= weight_factor  # Multiply weight by weight_factor for events within bin range

    weight = {"eta_weight": weight}
    return pd.DataFrame.from_dict(weight)


def get_alt_vertexing_conditions_B_P_PT(data_tuple, vertexing_network):

    session = ort.InferenceSession(f"{myGlobals.SYST_MODELS_PATH}map_model.onnx")

    alt_tuple = data_tuple.tuple.copy()

    P = alt_tuple.eval("sqrt(MOTHER_PX_TRUE**2+MOTHER_PY_TRUE**2+MOTHER_PZ_TRUE**2)")
    PT = alt_tuple.eval("sqrt(MOTHER_PX_TRUE**2+MOTHER_PY_TRUE**2)")
    eta = 0.5 * np.log(
        (P + alt_tuple["MOTHER_PZ_TRUE"]) / (P - alt_tuple["MOTHER_PZ_TRUE"])
    )

    inputs = {}
    inputs["PT"] = (np.log10(PT) + 2.8) / 5.4
    inputs["eta"] = (eta - 1) / 5.0
    inputs = pd.DataFrame.from_dict(inputs)

    model_input = np.asarray(inputs[["PT", "eta"]])

    input_data = {}
    input_data["input_PT_eta"] = model_input.astype(np.float32)

    model_output = session.run(["dense_3"], input_data)[0]

    shift_pt = np.asarray(model_output[:, 0] * 2.0 - 1.0) * (0.15)
    new_PT = np.power(10.0, (inputs["PT"] + shift_pt) * 5.4 - 2.8)

    shift_eta = np.asarray(model_output[:, 1] * 2.0 - 1.0) * (0.25)
    new_eta = (inputs["eta"] + shift_eta) * 5.0 + 1.0

    new_P = new_PT / np.sin(2 * np.arctan(np.exp(-new_eta)))

    theta = np.arctan2(
        alt_tuple["MOTHER_PY_TRUE"], alt_tuple["MOTHER_PX_TRUE"]
    )  # azimuthal angle
    new_PX = new_PT * np.cos(theta)
    new_PY = new_PT * np.sin(theta)
    new_PZ = np.sqrt(new_P**2 - new_PX**2 - new_PY**2)

    import vector  # need to use v0.8

    PE = np.sqrt(
        alt_tuple["MOTHER_M_TRUE"] ** 2
        + alt_tuple["MOTHER_PX_TRUE"] ** 2
        + alt_tuple["MOTHER_PY_TRUE"] ** 2
        + alt_tuple["MOTHER_PZ_TRUE"] ** 2
    )
    fmom_B = vector.obj(
        px=alt_tuple["MOTHER_PX_TRUE"],
        py=alt_tuple["MOTHER_PY_TRUE"],
        pz=alt_tuple["MOTHER_PZ_TRUE"],
        E=PE,
    )

    PE = np.sqrt(alt_tuple["MOTHER_M_TRUE"] ** 2 + new_PX**2 + new_PY**2 + new_PZ**2)
    fmom_B_NEW = vector.obj(px=new_PX, py=new_PY, pz=new_PZ, E=PE)

    # Boost DAUGHTERs
    for daughter in [1, 2, 3]:
        PE = np.sqrt(
            alt_tuple[f"DAUGHTER{daughter}_M_TRUE"] ** 2
            + alt_tuple[f"DAUGHTER{daughter}_PX_TRUE"] ** 2
            + alt_tuple[f"DAUGHTER{daughter}_PY_TRUE"] ** 2
            + alt_tuple[f"DAUGHTER{daughter}_PZ_TRUE"] ** 2
        )
        fmom_DAUGHTER = vector.obj(
            px=alt_tuple[f"DAUGHTER{daughter}_PX_TRUE"],
            py=alt_tuple[f"DAUGHTER{daughter}_PY_TRUE"],
            pz=alt_tuple[f"DAUGHTER{daughter}_PZ_TRUE"],
            E=PE,
        )
        fmom_DAUGHTER_com = fmom_DAUGHTER.boost_beta3(-fmom_B.to_beta3())
        fmom_DAUGHTER_NEW = fmom_DAUGHTER_com.boost_beta3(fmom_B_NEW.to_beta3())
        for dim in ["X", "Y", "Z"]:
            residual = (
                alt_tuple[f"DAUGHTER{daughter}_P{dim}"]
                - alt_tuple[f"DAUGHTER{daughter}_P{dim}_TRUE"]
            )
            if dim == "X":
                alt_tuple[f"DAUGHTER{daughter}_P{dim}_TRUE"] = fmom_DAUGHTER_NEW.px
            if dim == "Y":
                alt_tuple[f"DAUGHTER{daughter}_P{dim}_TRUE"] = fmom_DAUGHTER_NEW.py
            if dim == "Z":
                alt_tuple[f"DAUGHTER{daughter}_P{dim}_TRUE"] = fmom_DAUGHTER_NEW.pz
            alt_tuple[f"DAUGHTER{daughter}_P{dim}"] = (
                residual + alt_tuple[f"DAUGHTER{daughter}_P{dim}_TRUE"]
            )
        # recompute P PT, TRUE AND RECO
        alt_tuple[f"DAUGHTER{daughter}_P"] = alt_tuple.eval(
            f"sqrt(DAUGHTER{daughter}_PX**2 + DAUGHTER{daughter}_PY**2 + DAUGHTER{daughter}_PZ**2)"
        )
        alt_tuple[f"DAUGHTER{daughter}_P_TRUE"] = alt_tuple.eval(
            f"sqrt(DAUGHTER{daughter}_PX_TRUE**2 + DAUGHTER{daughter}_PY_TRUE**2 + DAUGHTER{daughter}_PZ_TRUE**2)"
        )
        alt_tuple[f"DAUGHTER{daughter}_PT"] = alt_tuple.eval(
            f"sqrt(DAUGHTER{daughter}_PX**2 + DAUGHTER{daughter}_PY**2)"
        )
        alt_tuple[f"DAUGHTER{daughter}_PT_TRUE"] = alt_tuple.eval(
            f"sqrt(DAUGHTER{daughter}_PX_TRUE**2 + DAUGHTER{daughter}_PY_TRUE**2)"
        )

    alt_tuple["MOTHER_PX"] = alt_tuple.eval(
        "DAUGHTER1_PX + DAUGHTER2_PX + DAUGHTER3_PX"
    )
    alt_tuple["MOTHER_PY"] = alt_tuple.eval(
        "DAUGHTER1_PY + DAUGHTER2_PY + DAUGHTER3_PY"
    )
    alt_tuple["MOTHER_PZ"] = alt_tuple.eval(
        "DAUGHTER1_PZ + DAUGHTER2_PZ + DAUGHTER3_PZ"
    )
    alt_tuple["MOTHER_P"] = alt_tuple.eval(
        "sqrt(MOTHER_PX**2 + MOTHER_PY**2 + MOTHER_PZ**2)"
    )
    alt_tuple["MOTHER_PT"] = alt_tuple.eval("sqrt(MOTHER_PX**2 + MOTHER_PY**2)")

    alt_tuple["MOTHER_PX_TRUE"] = new_PX
    alt_tuple["MOTHER_PY_TRUE"] = new_PY
    alt_tuple["MOTHER_PZ_TRUE"] = new_PZ
    alt_tuple["MOTHER_PT_TRUE"] = new_PT
    alt_tuple["MOTHER_P_TRUE"] = new_P

    data_tuple.append_conditional_information(external_tuple=alt_tuple)

    alt_vertexing_conditions = data_tuple.get_branches(
        vertexing_network.conditions,
        vertexing_network.Transformers,
        external_tuple=alt_tuple,
    )
    original_vertexing_conditions = data_tuple.get_branches(
        vertexing_network.conditions,
        vertexing_network.Transformers,
    )
    # hack to avoid recomputing origin vertex
    alt_vertexing_conditions["IP_MOTHER_true_vertex"] = original_vertexing_conditions[
        "IP_MOTHER_true_vertex"
    ]
    alt_vertexing_conditions["DIRA_MOTHER_true_vertex"] = original_vertexing_conditions[
        "DIRA_MOTHER_true_vertex"
    ]
    alt_vertexing_conditions = np.asarray(
        alt_vertexing_conditions[vertexing_network.conditions]
    )

    return alt_vertexing_conditions
