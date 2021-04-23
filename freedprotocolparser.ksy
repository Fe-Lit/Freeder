meta:
  id: freedprotocolparser
  file-extension: freed
  title: FREE-D Position Tracking Protocol
  endian: be
seq:
  - id: magic
    contents: [0xd1]
    doc: Camera position/orientation data
  - id: cam_id
    type: u1
  - id: pan_angle
    type: s3be
  - id: tilt_angle
    type: s3be
  - id: roll_angle
    type: s3be
  - id: x_pos
    type: s3be
  - id: y_pos
    type: s3be
  - id: z_pos
    type: s3be
    doc: Height
  - id: zoom
    type: s3be
  - id: focus 
    type: s3be
  - id: custom_value
    type: u2
    doc: User defined/assignable field
  - id: checksum
    type: u1
    
types:
    s3be:
      seq:
        - id: sign
          type: b1
        - id: ext_mod
          type: b23
      instances:
        value:
          value: (sign?ext_mod-(1<<23):ext_mod)