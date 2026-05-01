# NetBox AV Plugin

AV metadata and cable validation for NetBox endpoints.

This plugin intentionally does **not** add `xlr` or `sdi` to NetBox's built-in `type` choices. NetBox component type choices are scoped by component model, and upstream device-type YAML will still reject unknown type slugs. Instead, keep native NetBox endpoints/cables and attach AV semantics to them.

## Model

Use normal NetBox objects:

- Active SDI/XLR endpoints: `dcim.Interface` with `type: other`
- Passive SDI/BNC panels: `dcim.FrontPort` / `dcim.RearPort` with `type: bnc`
- Passive XLR panels: `dcim.FrontPort` / `dcim.RearPort` with `type: other`

Then add:

- **AV Port Profiles**: reusable definitions such as `3G-SDI Input over BNC`, `XLR Output`, `DMX 5-pin Thru`, `HDMI Input`, or `Speakon Output`
- **AV Port Assignments**: one profile attached to one native endpoint (`Interface`, `FrontPort`, or `RearPort`)

## Install locally

From your NetBox virtualenv or container build:

```bash
pip install -e /path/to/netbox-av-plugin
```

Enable the plugin:

```python
PLUGINS = [
    "netbox_av_plugin",
]
```

Run migrations:

```bash
/opt/netbox/netbox/manage.py migrate netbox_av_plugin
```

## Optional cable validation

To block obvious AV patching mistakes, enable the custom cable validator:

```python
CUSTOM_VALIDATORS = {
    "dcim.Cable": (
        "netbox_av_plugin.validators.AVCableValidator",
    ),
}
```

The validator only checks cables where both terminations have AV assignments. It rejects:

- signal mismatch, e.g. SDI to analog audio
- rate mismatch when both sides specify a rate, e.g. HD-SDI to 3G-SDI
- connector mismatch, e.g. BNC to XLR
- strict input-to-input or output-to-output connections

## Supported AV choices

Signals:

- `sdi`
- `analog-audio`
- `dmx`
- `hdmi`
- `speaker`
- `timecode`
- `genlock`
- `rs-422`

SDI rates:

- `sd-sdi`
- `hd-sdi`
- `3g-sdi`
- `6g-sdi`

Connectors:

- `bnc`
- `xlr`
- `dmx-3-pin`
- `dmx-5-pin`
- `hdmi`
- `speakon`
- `trs-1-4`
- `trs-3-5`
- `de-9`

The initial migration seeds common input/output profiles for these choices.

## Example profiles

- `3G-SDI Input over BNC`
  - signal: `sdi`
  - rate: `3g-sdi`
  - connector: `bnc`
  - direction: `input`
- `XLR Output`
  - signal: `analog-audio`
  - connector: `xlr`
  - direction: `output`
- `DMX 5-pin Thru`
  - signal: `dmx`
  - connector: `dmx-5-pin`
  - direction: `thru`
- `Speakon Output`
  - signal: `speaker`
  - connector: `speakon`
  - direction: `output`
- `Timecode Input over BNC`
  - signal: `timecode`
  - connector: `bnc`
  - direction: `input`
- `Genlock Input over BNC`
  - signal: `genlock`
  - connector: `bnc`
  - direction: `input`
- `1/4" Headphone Output`
  - signal: `analog-audio`
  - connector: `trs-1-4`
  - direction: `output`
- `RS-422 Input over DE-9`
  - signal: `rs-422`
  - connector: `de-9`
  - direction: `input`

## API

API routes:

- `/api/plugins/netbox-av-plugin/port-profiles/`
- `/api/plugins/netbox-av-plugin/port-assignments/`

## Notes

This plugin keeps NetBox cabling native. It does not create a parallel AV cable model, so existing NetBox cable tracing, device views, and API workflows remain usable.
