def get_values(*names):
    import json
    _all_values = json.loads("""{"num_columns":6,"num_plates":1}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'Standard Serial Dilution',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    [num_columns, num_plates] = get_values(  # noqa: F821
        "num_columns", "num_plates")

    if not 1 <= num_columns <= 12:
        raise Exception("Enter a column number between 1-12")
    if not 1 <= num_plates <= 10:
        raise Exception("Enter a plate number between 1-10")

    # custom number of Plates
    custom_plates = [str(i) for i in range(2, num_plates+2)]

    # labware setup
    tiprack = ctx.load_labware('opentrons_96_filtertiprack_20ul', '1')
    plates = [ctx.load_labware('corning_96_wellplate_360ul_flat', slot)
              for slot in custom_plates]

    # instrument setup
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack])

    # commands
    num_dilutions = num_columns - 1

    for plate in plates:
        p20.pick_up_tip()
        rows = zip(plate.rows()[0][:num_dilutions],
                   plate.rows()[0][1:num_dilutions+1])
        p20.mix(17, 10, plate.rows()[0][0].bottom(-2))
        for source, dest in rows:
            p20.transfer(1, source.bottom(-2), dest.bottom(-2),
                          mix_after=(17, 5), new_tip='never')
        p20.aspirate(1, plate.rows()[0][num_dilutions].bottom(-2))
        p20.drop_tip()
