"""Shorts cut from EP01 and EP02 (see tools/shorts.py)."""
EP1 = "/home/user/hyperframes/channel/ep01-3am-call/video/renders/the-3am-call_v3_final.mp4"
EP2 = "/home/user/hyperframes/channel/ep02-whiteout/video/renders/whiteout_v2_final.mp4"

SHORTS = [
    dict(id="ep01_r01_own_number", ep="ep01-3am-call", video=EP1, u0=36, u1=51,
         kicker="RULE 1 · THE 3:00 AM CALL", title="IF <y>YOUR OWN NUMBER</y> CALLS YOU AT 3:00 AM, <r>DON'T ANSWER</r>"),
    dict(id="ep01_r06_its_for_you", ep="ep01-3am-call", video=EP1, u0=126, u1=140, crop_w=1640,
         kicker="RULE 6 · THE 3:00 AM CALL", title="IF SOMEONE SAYS <y>“IT'S FOR YOU”</y>, <r>DON'T TAKE THE PHONE</r>"),
    dict(id="ep01_r11_payphones", ep="ep01-3am-call", video=EP1, u0=216, u1=230,
         kicker="RULE 11 · THE 3:00 AM CALL", title="NEVER PICK UP A <y>RINGING PAYPHONE</y>"),
    dict(id="ep02_r16_no_snow", ep="ep02-whiteout", video=EP2, u0=245, u1=265,
         kicker="RULE 16 · 40 DAYS OF SNOW", title="NO SNOW ON <y>HIS SHOULDERS</y>? <r>DON'T OPEN</r>"),
    dict(id="ep02_r07_footprints", ep="ep02-whiteout", video=EP2, u0=124, u1=133,
         kicker="RULE 7 · 40 DAYS OF SNOW", title="FOOTPRINTS LEAD <y>TO YOUR DOOR</y>. <r>NONE LEAD AWAY</r>."),
    dict(id="ep02_r19_birds", ep="ep02-whiteout", video=EP2, u0=293, u1=311,
         kicker="RULE 19 · 40 DAYS OF SNOW", title="WHEN THE SNOW STOPS, <y>WAIT FOR THE BIRDS</y>"),
]
