from zur_ecu_client.messages import *
from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_zur_names import SenmlNames
from zur_ecu_client.senml.senml_msg_dv import Dv
from zur_ecu_client.senml.senml_msg_ecu import Ecu
from zur_ecu_client.senml.senml import Senml


# Test parsing of all ECU messages
def test_parse_ecu_hvcb_sensor_msg():
    msg = Messages.parse(
        '[[{"bn":"ECU","n":"HVCB","vs":"sensor"}, {"n":"LVAccu","u":"V","v":0}, {"n":"24V","u":"V","v":0}, {"n":"12V",'
        '"u":"V","v":0}, {"n":"LVShutdown","vb":false}]]'
    )
    assert msg == {
        SenmlNames.ECU_HVCB_SENSOR_LVACCU: 0,
        SenmlNames.ECU_HVCB_SENSOR_24V: 0,
        SenmlNames.ECU_HVCB_SENSOR_12V: 0,
        SenmlNames.ECU_HVCB_SENSOR_LVSHUTDOWN: False,
    }


def test_parse_ecu_accu_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"accu","vs":"sensor"},{"n":"charge","u":"%","v":0},{"n":"temp","u":"Cel","v":0},'
        '{"n":"AIRPos","u":"V","v":0},{"n":"AIRNeg","u":"V","v":0},{"n":"preRelay","u":"V","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_ACCU_SENSOR_CHARGE: 0,
        SenmlNames.ECU_ACCU_SENSOR_TEMP: 0,
        SenmlNames.ECU_ACCU_SENSOR_AIRPOS: 0,
        SenmlNames.ECU_ACCU_SENSOR_AIRNEG: 0,
        SenmlNames.ECU_ACCU_SENSOR_PRERELAY: 0,
    }


def test_pare_ecu_cockpit_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"cockpit","vs":"sensor"},{"n":"x","u":"m/s2","v":0},{"n":"y","u":"m/s2","v":0},{"n":"z",'
        '"u":"m/s2","v":0}]'
    )
    assert msg == {
        SenmlNames.ECU_COCKPIT_X: 0,
        SenmlNames.ECU_COCKPIT_Y: 0,
        SenmlNames.ECU_COCKPIT_Z: 0,
    }


def test_parse_ecu_dv_sensor_msg():
    msg = Messages.parse(
        '[{"bn":"ECU","n":"DV","vs":"sensor"},{"n":"modeSel","vb":false},{"n":"modeACK","vb":false},{"n":"reset",'
        '"vb":false}]'
    )
    assert msg == {
        SenmlNames.ECU_DV_SENSOR_MODESEL: False,
        SenmlNames.ECU_DV_SENSOR_MODEACK: False,
        SenmlNames.ECU_DV_SENSOR_RESET: False,
    }


# Test parsing of all DV messages
def test_parse_dv_ctrl_msg():
    msg = Messages.parse(
        '[{"bn":"DV","n":"ctrl","vs":""}, {"n":"brake","u":"%","v":0}, {"n":"steering","u":"%","v":0}, '
        '{"n":"throttle","u":"%","v":0}, {"n":"status","vs":"Hello World!"}]'
    )
    assert msg == {
        SenmlNames.DV_CTRL_BRAKE: 0,
        SenmlNames.DV_CTRL_STEERING: 0,
        SenmlNames.DV_CTRL_THROTTLE: 0,
        SenmlNames.DV_CTRL_STATUS: "Hello World!",
    }


def test_parse_dv_cfg_msg():
    msg = Messages.parse(
        '[{"bn":"DV","n":"cfg", "vs":""},{"n":"AS","vs":"OFF"},{"n":"EBS","vs":"N/A"},{"n":"AMI","vs":"ACC"}]'
    )
    assert msg == {
        SenmlNames.DV_CFG_AS: "OFF",
        SenmlNames.DV_CFG_EBS: "N/A",
        SenmlNames.DV_CFG_AMI: "ACC",
    }


def test_parse_dv_stat_msg():
    msg = Messages.parse(
        '[{"bn":"DV", "n":"stat", "vs":""},{"n":"laps","v":0},{"n":"conesAct","v":0},{"n":"conesAll","v":0}]'
    )
    assert msg == {
        SenmlNames.DV_STAT_LAPS: 0,
        SenmlNames.DV_STAT_CONESACT: 0,
        SenmlNames.DV_STAT_CONESALL: 0,
    }


def test_parse_dv_acc_msg():
    msg = Messages.parse(
        '[{"bn":"DV", "n":"acc", "vs":""},{"n":"X","u":"m/s2","v":0},{"n":"Y","u":"m/s2","v":0},{"n":"Z","u":"m/s2",'
        '"v":0}]'
    )
    assert msg == {
        SenmlNames.DV_ACC_X: 0,
        SenmlNames.DV_ACC_Y: 0,
        SenmlNames.DV_ACC_Z: 0,
    }


# Test building of all DV messages
def test_build_dv_ctrl_msg():
    msg = Dv.Ctrl(0, 0, 0, "Hello World!").get()
    assert msg == [
        {"bn": "DV", "n": "ctrl", "vs": "controller"},
        {"n": "brake", "u": "%", "v": 0},
        {"n": "steering", "u": "%", "v": 0},
        {"n": "throttle", "u": "%", "v": 0},
        {"n": "status", "vs": "Hello World!"},
    ]


def test_build_dv_cfg_msg():
    msg = Dv.Cfg("OFF", "N/A", "ACC").get()
    assert msg == [
        {"bn": "DV", "n": "cfg", "vs": "controller"},
        {"n": "AS", "vs": "OFF"},
        {"n": "EBS", "vs": "N/A"},
        {"n": "AMI", "vs": "ACC"},
    ]


def test_build_dv_stat_msg():
    msg = Dv.Stat(0, 0, 0).get()
    assert msg == [
        {"bn": "DV", "n": "stat", "vs": "controller"},
        {"n": "laps", "v": 0},
        {"n": "conesAct", "v": 0},
        {"n": "conesAll", "v": 0},
    ]


def test_build_dv_acc_msg():
    msg = Dv.Acc(0, 0, 0).get()
    assert msg == [
        {"bn": "DV", "n": "acc", "vs": "controller"},
        {"n": "X", "u": "m/s2", "v": 0},
        {"n": "Y", "u": "m/s2", "v": 0},
        {"n": "Z", "u": "m/s2", "v": 0},
    ]


# Test building of all ECU messages
def test_build_ecu_hvcb_sensor_msg():
    msg = Ecu.Hvcb(0, 0, 0, False).get()
    assert msg == [
        {"bn": "ECU", "n": "HVCB", "vs": "sensor"},
        {"n": "LVAccu", "u": "V", "v": 0},
        {"n": "24V", "u": "V", "v": 0},
        {"n": "12V", "u": "V", "v": 0},
        {"n": "LVShutdown", "vb": False},
    ]


def test_build_ecu_accu_sensor_msg():
    msg = Ecu.Accu(0, 0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "accu", "vs": "sensor"},
        {"n": "charge", "u": "%", "v": 0},
        {"n": "temp", "u": "Cel", "v": 0},
        {"n": "AIRPos", "u": "V", "v": 0},
        {"n": "AIRNeg", "u": "V", "v": 0},
        {"n": "preRelay", "u": "V", "v": 0},
    ]


def test_build_ecu_pedal_sensor_msg():
    msg = Ecu.Pedal(0, 0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "pedal", "vs": "sensor"},
        {"n": "throttleLeft", "u": "%", "v": 0},
        {"n": "throttleRight", "u": "%", "v": 0},
        {"n": "brakeFront", "u": "%", "v": 0},
        {"n": "brakeBack", "u": "%", "v": 0},
    ]


def test_build_ecu_cockpit_sensor_msg():
    msg = Ecu.Cockpit(0, 0, 0).get()
    assert msg == [
        {"bn": "ECU", "n": "cockpit", "vs": "sensor"},
        {"n": "x", "u": "m/s2", "v": 0},
        {"n": "y", "u": "m/s2", "v": 0},
        {"n": "z", "u": "m/s2", "v": 0},
    ]


def test_build_ecu_dv_sensor_msg():
    msg = Ecu.Dv(False, False, False).get()
    assert msg == [
        {"bn": "ECU", "n": "DV", "vs": "sensor"},
        {"n": "modeSel", "vb": False},
        {"n": "modeACK", "vb": False},
        {"n": "reset", "vb": False},
    ]
