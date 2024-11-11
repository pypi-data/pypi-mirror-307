from zur_ecu_client.messages import Acknowledgment, Data, Messages
from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_zur_names import SenmlNames


def test_incoming_parser():
    msg = Messages.parse(
        """
        [
            [
                {"bn": "DV", "n": "ctrl", "v": "sensor"}
            ],
            [
                {"bn": "ECU", "n": "accu", "vs": "sensor"},
                {"n": "charge", "u": "%", "v": 0},
                {"n": "temp", "u": "Cel", "v": 0},
                {"n": "AIRPos", "u": "V", "v": 0},
                {"n": "AIRNeg", "u": "V", "v": 0},
                {"n": "preRelay", "u": "V", "v": 0}
            ]
        ]"""
    )

    assert msg == {
        SenmlNames.ECU_ACCU_SENSOR_CHARGE: 0,
        SenmlNames.ECU_ACCU_SENSOR_TEMP: 0,
        SenmlNames.ECU_ACCU_SENSOR_AIRPOS: 0,
        SenmlNames.ECU_ACCU_SENSOR_AIRNEG: 0,
        SenmlNames.ECU_ACCU_SENSOR_PRERELAY: 0,
    }


def test_incoming_parser_single_list_message():
    msg = Messages.parse(
        """
        [
            {"bn": "DV", "n": "ctrl", "v": "sensor"},
            {"bn": "ECU", "n": "accu", "vs": "sensor"},
            {"n": "charge", "u": "%", "v": 0},
            {"n": "temp", "u": "Cel", "v": 0},
            {"n": "AIRPos", "u": "V", "v": 0},
            {"n": "AIRNeg", "u": "V", "v": 0},
            {"n": "preRelay", "u": "V", "v": 0}
        ]"""
    )

    assert msg == {
        SenmlNames.ECU_ACCU_SENSOR_CHARGE: 0,
        SenmlNames.ECU_ACCU_SENSOR_TEMP: 0,
        SenmlNames.ECU_ACCU_SENSOR_AIRPOS: 0,
        SenmlNames.ECU_ACCU_SENSOR_AIRNEG: 0,
        SenmlNames.ECU_ACCU_SENSOR_PRERELAY: 0,
    }
