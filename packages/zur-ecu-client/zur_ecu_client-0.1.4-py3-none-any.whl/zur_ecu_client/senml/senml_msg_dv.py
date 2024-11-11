from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_msg import SenmlMessage
from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_zur_names import SenmlNames


class Dv:
    class Control(SenmlMessage):
        def __init__(
            self, brake: int = None, steering: int = None, throttle: int = None
        ) -> None:
            super().__init__(
                SenmlNames.DV_CONTROL,
                [
                    Senml.Record(SenmlNames.DV_CONTROL_BRAKE, v=brake),
                    Senml.Record(SenmlNames.DV_CONTROL_STEERING, v=steering),
                    Senml.Record(SenmlNames.DV_CONTROL_THROTTLE, v=throttle),
                ],
            )

    # TODO remove (depricated)
    class Cfg(SenmlMessage):
        def __init__(
            self,
            ass: str = None,
            ebss: str = None,
            asms: str = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_CFG,
                [
                    Senml.Record(
                        SenmlNames.DV_CFG_AS,
                        v=ass,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CFG_EBS,
                        v=ebss,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CFG_AMI,
                        v=asms,
                    ),
                ],
            )

    # TODO remove (depricated)
    class Ctrl(SenmlMessage):
        def __init__(
            self,
            brake: int = None,
            steering: int = None,
            throttle: int = None,
            status: str = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_CTRL,
                [
                    Senml.Record(
                        SenmlNames.DV_CTRL_BRAKE,
                        SenmlUnit.PERCENTAGE,
                        brake,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CTRL_STEERING,
                        SenmlUnit.PERCENTAGE,
                        steering,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CTRL_THROTTLE,
                        SenmlUnit.PERCENTAGE,
                        throttle,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CTRL_STATUS,
                        v=status,
                    ),
                ],
            )

    # TODO remove (depricated)
    class Stat(SenmlMessage):
        def __init__(
            self,
            laps: int = None,
            cones_actual: int = None,
            cones_all: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_STAT,
                [
                    Senml.Record(
                        SenmlNames.DV_STAT_LAPS,
                        v=laps,
                    ),
                    Senml.Record(
                        SenmlNames.DV_STAT_CONESACT,
                        v=cones_actual,
                    ),
                    Senml.Record(
                        SenmlNames.DV_STAT_CONESALL,
                        v=cones_all,
                    ),
                ],
            )

    # TODO remove (depricated)
    class Acc(SenmlMessage):
        def __init__(
            self,
            x: int = None,
            y: int = None,
            z: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_ACC,
                [
                    Senml.Record(
                        SenmlNames.DV_ACC_X,
                        SenmlUnit.ACCELERATION,
                        x,
                    ),
                    Senml.Record(
                        SenmlNames.DV_ACC_Y,
                        SenmlUnit.ACCELERATION,
                        y,
                    ),
                    Senml.Record(
                        SenmlNames.DV_ACC_Z,
                        SenmlUnit.ACCELERATION,
                        z,
                    ),
                ],
            )
