from opentrons import protocol_api


metadata = {
    'protocolName': 'NEW Standard Serial Dilution Test',
    'author': 'Sydney Lam',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol: protocol_api.ProtocolContext):

    # labware setup
    tiprack = protocol.load_labware('opentrons_96_filtertiprack_20ul', 1)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)


    # instrument setup
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack])

    # commands
    for i in range(8):
       
        row = plate.rows()[i]
        p20.pick_up_tip()
        p20.mix(15, 10, row[0].bottom(-2))
        p20.blow_out()
        p20.touch_tip()
        p20.blow_out(row[0].bottom(1))
        p20.blow_out(row[0].bottom(1))
        p20.blow_out(row[0].bottom(1))
        protocol.delay(seconds=3)

        for j in range(5):
            p20.aspirate(1, row[j].bottom(-2), rate=0.75)
            p20.air_gap(1)
            p20.dispense(2, row[j+1], rate=2.0)
            protocol.delay(seconds=3)
            p20.blow_out(row[j+1].bottom(1))
            p20.mix(10, 5, row[j+1].bottom(-2))

            p20.blow_out(row[j+1].bottom(1))
            p20.mix(7, 5, row[j+1].bottom(-2))

            p20.blow_out(row[j+1].bottom(1))
            p20.blow_out(row[j+1])
            p20.touch_tip(row[j+1])
            protocol.delay(seconds=3)
            p20.blow_out(row[j+1].bottom(1))

        p20.drop_tip()
        
        
        
