from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_msg import SenmlMessage
from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_zur_names import SenmlNames


class Ecu:
    class Hvcb(SenmlMessage):
        def __init__(
            self,
            lv_accu: int = None,
            v24: int = None,
            v12: int = None,
            lv_shutdown: bool = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_HVCB_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_HVCB_SENSOR_LVACCU,
                        SenmlUnit.VOLT,
                        lv_accu,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_HVCB_SENSOR_24V,
                        SenmlUnit.VOLT,
                        v24,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_HVCB_SENSOR_12V,
                        SenmlUnit.VOLT,
                        v12,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_HVCB_SENSOR_LVSHUTDOWN,
                        v=lv_shutdown,
                    ),
                ],
            )

    class Pedal(SenmlMessage):
        def __init__(
            self,
            throttle_left: int = None,
            throttle_right: int = None,
            brake_front: int = None,
            brake_back: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_PEDAL,
                [
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_THROTTLE_LEFT,
                        SenmlUnit.PERCENTAGE,
                        throttle_left,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_THROTTLE_RIGHT,
                        SenmlUnit.PERCENTAGE,
                        throttle_right,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_BRAKE_FRONT,
                        SenmlUnit.PERCENTAGE,
                        brake_front,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_PEDAL_BRAKE_BACK,
                        SenmlUnit.PERCENTAGE,
                        brake_back,
                    ),
                ],
            )

    class Accu(SenmlMessage):
        def __init__(
            self,
            charge: int = None,
            temp: int = None,
            air_pos: int = None,
            air_neg: int = None,
            pre_relay: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_ACCU_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_CHARGE,
                        SenmlUnit.PERCENTAGE,
                        charge,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_TEMP,
                        SenmlUnit.DEGREES_CELSIUS,
                        temp,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_AIRPOS,
                        SenmlUnit.VOLT,
                        air_pos,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_AIRNEG,
                        SenmlUnit.VOLT,
                        air_neg,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_ACCU_SENSOR_PRERELAY,
                        SenmlUnit.VOLT,
                        pre_relay,
                    ),
                ],
            )

    class Cockpit(SenmlMessage):
        def __init__(
            self,
            x: int = None,
            y: int = None,
            z: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_COCKPIT,
                [
                    Senml.Record(
                        SenmlNames.ECU_COCKPIT_X,
                        SenmlUnit.ACCELERATION,
                        x,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_COCKPIT_Y,
                        SenmlUnit.ACCELERATION,
                        y,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_COCKPIT_Z,
                        SenmlUnit.ACCELERATION,
                        z,
                    ),
                ],
            )

    class Dv(SenmlMessage):
        def __init__(
            self,
            mode_sel: bool = None,
            mode_ack: bool = None,
            reset: bool = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_DV_SENSOR,
                [
                    Senml.Record(
                        SenmlNames.ECU_DV_SENSOR_MODESEL,
                        v=mode_sel,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_DV_SENSOR_MODEACK,
                        v=mode_ack,
                    ),
                    Senml.Record(
                        SenmlNames.ECU_DV_SENSOR_RESET,
                        v=reset,
                    ),
                ],
            )

    class Error(SenmlMessage):
        def __init__(self, error_message: str = None, error_icon: str = None) -> None:
            super().__init__(
                SenmlNames.ECU_ERROR_INFO,
                [
                    Senml.Record(SenmlNames.ECU_ERROR_INFO_ICON, v=error_icon),
                    Senml.Record(
                        SenmlNames.ECU_ERROR_INFO_MESSAGE,
                        v=error_message,
                    ),
                ],
            )

    class Inverter(SenmlMessage):
        def __init__(
            self,
            velocity: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_INVERTER_ACTUAL,
                [
                    Senml.Record(SenmlNames.ECU_INVERTER_ACTUAL_VELOCITY, v=velocity),
                ],
            )

    # TODO resolve temporary message definitions
    class Temporary(SenmlMessage):
        def __init__(
            self,
            available: bool = False,
            mission_sel: int = None,
            mission_ack: int = None,
            startup: bool = False,
            shutdown: bool = False,
        ) -> None:
            super().__init__(
                SenmlNames.ECU_TEMPORARY_INFO,
                [
                    Senml.Record(SenmlNames.ECU_TEMPORARY_INFO_AVAILABLE, v=available),
                    Senml.Record(
                        SenmlNames.ECU_TEMPORARY_INFO_MISSION_SEL, v=mission_sel
                    ),
                    Senml.Record(
                        SenmlNames.ECU_TEMPORARY_INFO_MISSION_ACK, v=mission_ack
                    ),
                    Senml.Record(SenmlNames.ECU_TEMPORARY_INFO_STARTUP, v=startup),
                    Senml.Record(SenmlNames.ECU_TEMPORARY_INFO_SHUTDOWN, v=shutdown),
                ],
            )
