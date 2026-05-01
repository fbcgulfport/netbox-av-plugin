from utilities.choices import ChoiceSet


class AVSignalChoices(ChoiceSet):
    SIGNAL_SDI = "sdi"
    SIGNAL_ANALOG_AUDIO = "analog-audio"
    SIGNAL_DMX = "dmx"
    SIGNAL_HDMI = "hdmi"
    SIGNAL_SPEAKER = "speaker"
    SIGNAL_TIMECODE = "timecode"
    SIGNAL_GENLOCK = "genlock"
    SIGNAL_RS_422 = "rs-422"

    CHOICES = (
        (SIGNAL_SDI, "SDI", "blue"),
        (SIGNAL_ANALOG_AUDIO, "Analog Audio", "green"),
        (SIGNAL_DMX, "DMX", "purple"),
        (SIGNAL_HDMI, "HDMI", "orange"),
        (SIGNAL_SPEAKER, "Speaker", "cyan"),
        (SIGNAL_TIMECODE, "Timecode", "yellow"),
        (SIGNAL_GENLOCK, "Genlock / Reference", "teal"),
        (SIGNAL_RS_422, "RS-422", "gray"),
    )


class AVRateChoices(ChoiceSet):
    RATE_SDI_SD = "sd-sdi"
    RATE_SDI_HD = "hd-sdi"
    RATE_SDI_3G = "3g-sdi"
    RATE_SDI_6G = "6g-sdi"

    CHOICES = (
        (RATE_SDI_SD, "SD-SDI"),
        (RATE_SDI_HD, "HD-SDI"),
        (RATE_SDI_3G, "3G-SDI"),
        (RATE_SDI_6G, "6G-SDI"),
    )


class AVConnectorChoices(ChoiceSet):
    CONNECTOR_BNC = "bnc"
    CONNECTOR_XLR = "xlr"
    CONNECTOR_DMX_3_PIN = "dmx-3-pin"
    CONNECTOR_DMX_5_PIN = "dmx-5-pin"
    CONNECTOR_HDMI = "hdmi"
    CONNECTOR_SPEAKON = "speakon"
    CONNECTOR_TRS_1_4 = "trs-1-4"
    CONNECTOR_TRS_3_5 = "trs-3-5"
    CONNECTOR_DE_9 = "de-9"

    CHOICES = (
        (CONNECTOR_BNC, "BNC", "blue"),
        (CONNECTOR_XLR, "XLR", "green"),
        (CONNECTOR_DMX_3_PIN, "DMX 3-pin", "purple"),
        (CONNECTOR_DMX_5_PIN, "DMX 5-pin", "purple"),
        (CONNECTOR_HDMI, "HDMI", "orange"),
        (CONNECTOR_SPEAKON, "Speakon", "cyan"),
        (CONNECTOR_TRS_1_4, '1/4" TRS', "green"),
        (CONNECTOR_TRS_3_5, "3.5mm TRS", "green"),
        (CONNECTOR_DE_9, "DE-9", "gray"),
    )


class AVDirectionChoices(ChoiceSet):
    DIRECTION_INPUT = "input"
    DIRECTION_OUTPUT = "output"
    DIRECTION_BIDIRECTIONAL = "bidirectional"
    DIRECTION_THRU = "thru"

    CHOICES = (
        (DIRECTION_INPUT, "Input", "green"),
        (DIRECTION_OUTPUT, "Output", "blue"),
        (DIRECTION_BIDIRECTIONAL, "Bidirectional", "purple"),
        (DIRECTION_THRU, "Thru", "cyan"),
    )


class AVGenderChoices(ChoiceSet):
    GENDER_FEMALE = "female"
    GENDER_MALE = "male"
    GENDER_NONE = "none"
    GENDER_UNKNOWN = "unknown"

    CHOICES = (
        (GENDER_FEMALE, "Female"),
        (GENDER_MALE, "Male"),
        (GENDER_NONE, "N/A"),
        (GENDER_UNKNOWN, "Unknown"),
    )
