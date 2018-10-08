import cairo
import pint
import math
from collections import namedtuple

units = pint.UnitRegistry()
LineStyle = namedtuple("LineStyle", "width color dash")
MountingHole = namedtuple("MountingHole", "screw_diameter hole_diameter nut_width nut_height")

M3_MOUNTING_HOLE = MountingHole(
    screw_diameter = 3.0 * units.mm,
    hole_diameter = 3.125 * units.mm,
    nut_width = 5.5 * units.mm,
    nut_height = 6.01 * units.mm
)

M2_MOUNTING_HOLE = MountingHole(
    screw_diameter = 2.0 * units.mm,
    hole_diameter = 2.083 * units.mm,
    nut_width = 4.0 * units.mm,
    nut_height = 4.32 * units.mm
)

MOUNTING_HOLE_GUIDE_STYLE = LineStyle(
    width = 0.1 * units.mm,
    color = (0.0, 1.0, 0.0, 1.0),
    dash = None
)

GOLDEN_RATIO = 1.61803398875

CANVAS_WIDTH = 70 * units.mm
CANVAS_HEIGHT = 36 * 5 * units.mm
CORNER_ROUNDING_RADIUS = 2.5 * units.mm
M3_HOLE_DIAMETER = 3.125 * units.mm
CHASSIS_BASIC_WIDTH = 69.0 * units.mm
CHASSIS_BASIC_BREADTH = GOLDEN_RATIO * CHASSIS_BASIC_WIDTH - 15.0 * units.mm
CHASSIS_THICKNESS = 0.05 * units.inch

# board dimensions
BOARD_WIDTH = 53.3 * units.mm
BOARD_BREADTH_MIN = 66.3 * units.mm # check this dimension
BOARD_BREADTH_MAX = 68.6 * units.mm
BOARD_RECESSED_SHORT_SEGMENT = 2.5 * units.mm
BOARD_RECESSED_LONG_SEGMENT = 12.404 * units.mm
BOARD_EXTENDED_SEGMENT = 33.5 * units.mm
BOARD_ANGLED_SEGMENT = 3.25 * units.mm
# (x, y) center relative to the corner with DC barrel jack
# positive x goes from DC barrel jack to USB connector
# positive y goes across the long side of the board
BOARD_MOUNTING_HOLES = (
    (2.25 * units.mm, 13.5 * units.mm),
    (50.75 * units.mm, 14.5 * units.mm),
    (7.25 * units.mm, 66.048 * units.mm),
#    (33.5 * units.mm, 66.048 * units.mm) # this one is wrong
)
BOARD_OUTLINE_STYLE = LineStyle(
    width = 0.1 * units.mm,
    color = (0.25, 0.25, 0.25, 1.0),
    dash = (1.0 * units.mm, 0.5 * units.mm)
)
BOARD_CLEARANCE_WITH_BOTTOM_EDGE = 2 * units.mm

CASTER_WHEEL_MOUNTING_WIDTH = 30.0 * units.mm
CASTER_WHEEL_MOUNTING_BREADTH = 24.3 * units.mm
CASTER_WHEEL_EDGE_DISTANCE = 3.0 * units.mm
CASTER_WHEEL_EXTRUSION = 5.5 * units.mm

CUT_LINE_STYLE = LineStyle(
    width = 0.1 * units.mm,
    color = (1.0, 0.0, 0.0, 1.0),
    dash = None
)

MAJOR_GRID_STYLE = LineStyle(
    width = 0.1 * units.mm,
    color = (0.9, 0.9, 0.9, 1.0),
    dash = None
)
MAJOR_GRID_SPACING = 5.0 * units.mm

MINOR_GRID_STYLE = LineStyle(
    width = 0.05 * units.mm,
    color = (0.9, 0.9, 0.9, 0.75),
    dash = (0.1 * units.mm, 0.1 * units.mm)
)
MINOR_GRID_SPACING = 1.0 * units.mm

BATTERY_WIDTH = 33.25 * units.mm
BATTERY_HOLE_CLEARANCE = 2.0 * units.mm
BATTERY_MOUNTING_HOLE = M3_MOUNTING_HOLE._replace(nut_width=None, nut_height=None)
BATTERY_CONNECTOR_HOLE = MountingHole(
    screw_diameter = 15.0 * units.mm,
    hole_diameter = 15.0 * units.mm,
    nut_width = None,
    nut_height = None
)

MOTOR_MOUNTING_WIDTH = 10.0 * units.mm
MOTOR_MOUNTING_BREADTH = 12.0 * units.mm
MOTOR_MOUNTING_EDGE_CLEARANCE = 2.0 * units.mm

MARKER_WIDTH = 8.7 * units.mm
SERVO_MOUNT_HOLE_CLEARANCE = 1.0 * units.mm
SERVO_MOUNT_BREADTH = 22.5 * units.mm + 2 * (2 * SERVO_MOUNT_HOLE_CLEARANCE + M3_MOUNTING_HOLE.nut_width)
SERVO_MOUNT_CENTER_OFFSET = 14.5 * units.mm + 0.5 * MARKER_WIDTH
SERVO_MOUNTING_SHELF_WIDTH = 4.7 * units.mm
SERVO_MOUNTING_SHELF_HEIGHT = 11.8 * units.mm
SERVO_MOUNTING_SHELF_DEPTH = 2.5 * units.mm
SERVO_BODY_WIDTH = 22.5 * units.mm
SERVO_INSET_WIDTH_MINOR = 6.0 * units.mm
SERVO_INSET_WIDTH_MAJOR = SERVO_BODY_WIDTH + 2 * SERVO_INSET_WIDTH_MINOR
SERVO_INSET_HEIGHT = SERVO_INSET_WIDTH_MINOR + CHASSIS_THICKNESS + SERVO_MOUNTING_SHELF_HEIGHT
SERVO_INSET_CLEARANCE = 0.2 * units.mm

FOR_LASER_CUTTER = False
if FOR_LASER_CUTTER:
    MOUNTING_HOLE_GUIDES = False
    BOARD_OUTLINE = False
    MAJOR_GRID = False
    MINOR_GRID = False
    CUT_LINE_STYLE = CUT_LINE_STYLE._replace(width = 0.01 * units.mm)
else:
    MOUNTING_HOLE_GUIDES = True
    BOARD_OUTLINE = True
    MAJOR_GRID = True
    MINOR_GRID = True

TESSELATION = True
TESSELATION_CANVAS_WIDTH = 14 * units.inch
TESSELATION_CANVAS_HEIGHT = 11 * units.inch
TESSELATION_COUNT_H = 5
TESSELATION_COUNT_V = 2
TESSELATION_OFFSET_X = CHASSIS_BASIC_WIDTH + 2 * units.mm
TESSELATION_OFFSET_Y = CHASSIS_BASIC_BREADTH + SERVO_MOUNT_BREADTH + 1.0 * units.mm

def PTS(x):
    y = x.to(units.points).magnitude
    assert(y >= 0)
    assert(y <= CANVAS_WIDTH.to(units.points).magnitude or y <= CANVAS_HEIGHT.to(units.points).magnitude)
    return y

def load_line_style(context, style):
    context.set_line_width(PTS(style.width))
    context.set_source_rgba(*style.color)
    if style.dash is None:
        context.set_dash(tuple())
    else:
        context.set_dash(PTS(d) for d in style.dash)

def draw_mounting_hole(context, hole, cx, cy):
    if MOUNTING_HOLE_GUIDES:
        load_line_style(context, MOUNTING_HOLE_GUIDE_STYLE)
        context.arc(
            PTS(cx),
            PTS(cy),
            PTS(0.5 * hole.screw_diameter),
            0,
            2.0 * math.pi
        )
        context.stroke()
        if hole.nut_width and hole.nut_height:
            s = (0.5 * hole.nut_width) / math.sin(math.pi / 3)
            dx = 0.5 * hole.nut_width
            dy = (0.5 * hole.nut_width) / math.tan(math.pi / 3)
            context.move_to(
                PTS(cx),
                PTS(cy - 0.5 * hole.nut_height)
            )
            context.rel_line_to(
                PTS(dx),
                PTS(dy)
            )
            context.rel_line_to(
                0,
                PTS(s)
            )
            context.rel_line_to(
                -PTS(dx),
                PTS(dy)
            )
            context.rel_line_to(
                -PTS(dx),
                -PTS(dy)
            )
            context.rel_line_to(
                0,
                -PTS(s)
            )
            context.rel_line_to(
                PTS(dx),
                -PTS(dy)
            )
            context.stroke()
    load_line_style(context, CUT_LINE_STYLE)
    context.arc(
        PTS(cx),
        PTS(cy),
        PTS(0.5 * hole.hole_diameter),
        0,
        2.0 * math.pi
    )
    context.stroke()

def draw_rect(context, top, bottom, left, right):
    context.move_to(
        PTS(left),
        PTS(bottom)
    )

    context.line_to(
        PTS(left),
        PTS(top)
    )

    context.line_to(
        PTS(right),
        PTS(top)
    )

    context.line_to(
        PTS(right),
        PTS(bottom)
    )

    context.line_to(
        PTS(left),
        PTS(bottom)
    )
    context.close_path()
    context.stroke()

def render(context):
    chassis_top = 0.5 * (CANVAS_HEIGHT - CHASSIS_BASIC_BREADTH - CASTER_WHEEL_EXTRUSION)
    chassis_bottom = chassis_top + CHASSIS_BASIC_BREADTH
    chassis_left = 0.5 * (CANVAS_WIDTH - CHASSIS_BASIC_WIDTH)
    chassis_right = chassis_left + CHASSIS_BASIC_WIDTH
    chassis_hcenter = 0.5 * (chassis_left + chassis_right)
    chassis_vcenter = 0.5 * (chassis_top + chassis_bottom)

    servo_mount_bottom = chassis_top
    servo_mount_top = servo_mount_bottom - SERVO_MOUNT_BREADTH
    left_servo_mount_left = chassis_left
    left_servo_mount_right = chassis_hcenter - SERVO_MOUNT_CENTER_OFFSET
    right_servo_mount_left = chassis_hcenter + SERVO_MOUNT_CENTER_OFFSET
    right_servo_mount_right = chassis_right

    context.save()

    if MINOR_GRID:
        x = 0.0 * units.mm
        load_line_style(context, MINOR_GRID_STYLE)
        while x <= CANVAS_WIDTH:
            context.move_to(
                PTS(x),
                0
            )
            context.line_to(
                PTS(x),
                PTS(CANVAS_HEIGHT)
            )
            context.stroke()
            x += MINOR_GRID_SPACING

        y = 0.0 * units.mm
        while y <= CANVAS_HEIGHT:
            context.move_to(
                0,
                PTS(y)
            )
            context.line_to(
                PTS(CANVAS_WIDTH),
                PTS(y)
            )
            context.stroke()
            y += MINOR_GRID_SPACING

    if MAJOR_GRID:
        x = 0.0 * units.mm
        load_line_style(context, MAJOR_GRID_STYLE)
        while x <= CANVAS_WIDTH:
            context.move_to(
                PTS(x),
                0
            )
            context.line_to(
                PTS(x),
                PTS(CANVAS_HEIGHT)
            )
            context.stroke()
            x += MAJOR_GRID_SPACING

        y = 0.0 * units.mm
        while y <= CANVAS_HEIGHT:
            context.move_to(
                0,
                PTS(y)
            )
            context.line_to(
                PTS(CANVAS_WIDTH),
                PTS(y)
            )
            context.stroke()
            y += MAJOR_GRID_SPACING

    # top left corner of left servo mount
    context.arc(
        PTS(left_servo_mount_left + CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.0 * math.pi,
        1.5 * math.pi
    )

    # top edge of left servo mount
    context.line_to(
        PTS(left_servo_mount_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_top)
    )

    # top right corner of left servo mount
    context.arc(
        PTS(left_servo_mount_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.5 * math.pi,
        2.0 * math.pi
    )

    # right edge of left servo mount
    context.line_to(
        PTS(left_servo_mount_right),
        PTS(servo_mount_bottom - CORNER_ROUNDING_RADIUS)
    )

    # bottom right corner of left servo mount
    context.arc_negative(
        PTS(left_servo_mount_right + CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.0 * math.pi,
        0.5 * math.pi
    )

    # chassis top
    context.line_to(
        PTS(right_servo_mount_left - CORNER_ROUNDING_RADIUS),
        PTS(chassis_top)
    )

    # bottom left corner of right servo mount
    context.arc_negative(
        PTS(right_servo_mount_left - CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0.5 * math.pi,
        0
    )

    # left edge of right servo mount
    context.line_to(
        PTS(right_servo_mount_left),
        PTS(servo_mount_top + CORNER_ROUNDING_RADIUS)
    )

    # top left corner of right servo mount
    context.arc(
        PTS(right_servo_mount_left + CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.0 * math.pi,
        1.5 * math.pi
    )

    # top edge of right servo mount
    context.line_to(
        PTS(right_servo_mount_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_top)
    )

    # top right corner of right servo mount
    context.arc(
        PTS(right_servo_mount_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_mount_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.5 * math.pi,
        2.0 * math.pi
    )

    # right edge of right servo mount and chassis
    context.line_to(
        PTS(chassis_right),
        PTS(chassis_bottom - CORNER_ROUNDING_RADIUS)
    )

    # bottom right corner
    context.arc(
        PTS(chassis_right - CORNER_ROUNDING_RADIUS),
        PTS(chassis_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0,
        0.5 * math.pi
    )

    caster_extrusion_top = chassis_bottom
    caster_extrusion_bottom = chassis_bottom + CASTER_WHEEL_EXTRUSION + CASTER_WHEEL_EDGE_DISTANCE
    caster_extrusion_width = CASTER_WHEEL_MOUNTING_WIDTH + 2 * CASTER_WHEEL_EDGE_DISTANCE
    caster_extrusion_left = chassis_left + 0.5 * (CHASSIS_BASIC_WIDTH - caster_extrusion_width)
    caster_extrusion_right = caster_extrusion_left + caster_extrusion_width
    # bottom edge to extrusion
    context.line_to(
        PTS(caster_extrusion_right + CORNER_ROUNDING_RADIUS),
        PTS(chassis_bottom)
    )

    # inner right corner of extrusion
    context.arc_negative(
        PTS(caster_extrusion_right + CORNER_ROUNDING_RADIUS),
        PTS(chassis_bottom + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.5 * math.pi,
        1.0 * math.pi
    )

    # right edge of extrusion
    context.line_to(
        PTS(caster_extrusion_right),
        PTS(caster_extrusion_bottom - CORNER_ROUNDING_RADIUS)
    )

    # outer right corner of extrusion
    context.arc(
        PTS(caster_extrusion_right - CORNER_ROUNDING_RADIUS),
        PTS(caster_extrusion_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0,
        0.5 * math.pi
    )

    # bottom edge of extrusion
    context.line_to(
        PTS(caster_extrusion_left + CORNER_ROUNDING_RADIUS),
        PTS(caster_extrusion_bottom)
    )

    # outer left corner of extrusion
    context.arc(
        PTS(caster_extrusion_left + CORNER_ROUNDING_RADIUS),
        PTS(caster_extrusion_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0.5 * math.pi,
        1.0 * math.pi
    )

    # left edge of extrusion
    context.line_to(
        PTS(caster_extrusion_left),
        PTS(caster_extrusion_top + CORNER_ROUNDING_RADIUS)
    )

    # inner left corner of extrusion
    context.arc_negative(
        PTS(caster_extrusion_left - CORNER_ROUNDING_RADIUS),
        PTS(caster_extrusion_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        2.0 * math.pi,
        1.5 * math.pi
    )

    # rest of the chassis bottom edge
    context.line_to(
        PTS(chassis_left + CORNER_ROUNDING_RADIUS),
        PTS(chassis_bottom)
    )

    # bottom left corner
    context.arc(
        PTS(chassis_left + CORNER_ROUNDING_RADIUS),
        PTS(chassis_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0.5 * math.pi,
        math.pi
    )

    # left edge
    context.line_to(
        PTS(chassis_left),
        PTS(chassis_top + CORNER_ROUNDING_RADIUS)
    )

    context.close_path()
    load_line_style(context, CUT_LINE_STYLE)
    context.stroke()


    servo_holder_bottom = chassis_top - 1.0 * units.mm
    servo_holder_left = chassis_hcenter - 0.5 * SERVO_INSET_WIDTH_MAJOR
    servo_left_prong_right = servo_holder_left + SERVO_INSET_WIDTH_MINOR
    servo_holder_right = servo_holder_left + SERVO_INSET_WIDTH_MAJOR
    servo_right_prong_left = servo_holder_right - SERVO_INSET_WIDTH_MINOR
    servo_holder_top = servo_holder_bottom - SERVO_INSET_HEIGHT

    # bottom left corner of servo holder
    context.arc(
        PTS(servo_holder_left + CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0.5 * math.pi,
        1.0 * math.pi
    )

    # left edge of servo holder
    context.line_to(
        PTS(servo_holder_left),
        PTS(servo_holder_top + CORNER_ROUNDING_RADIUS)
    )

    # top left corner of servo holder
    context.arc(
        PTS(servo_holder_left + CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.0 * math.pi,
        1.5 * math.pi
    )

    # top edge of servo holder left prong
    context.line_to(
        PTS(servo_left_prong_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_top)
    )

    # top right edge of servo holder left prong
    context.arc(
        PTS(servo_left_prong_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.5 * math.pi,
        2.0 * math.pi
    )

    # inner U shape for servo holder prong
    context.line_to(
        PTS(servo_left_prong_right),
        PTS(servo_holder_bottom - SERVO_INSET_WIDTH_MINOR)
    )
    context.line_to(
        PTS(servo_right_prong_left),
        PTS(servo_holder_bottom - SERVO_INSET_WIDTH_MINOR)
    )
    context.line_to(
        PTS(servo_right_prong_left),
        PTS(servo_holder_top + CORNER_ROUNDING_RADIUS)
    )

    # top left corner of servo holder right prong
    context.arc(
        PTS(servo_right_prong_left + CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.0 * math.pi,
        1.5 * math.pi
    )

    # top edge of servo holder right prong
    context.line_to(
        PTS(servo_holder_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_top)
    )

    # top right corner of servo holder right prong
    context.arc(
        PTS(servo_holder_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_top + CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        1.5 * math.pi,
        2.0 * math.pi
    )

    # right edge of servo holder
    context.line_to(
        PTS(servo_holder_right),
        PTS(servo_holder_bottom - CORNER_ROUNDING_RADIUS)
    )

    # bottom right corner of servo holder
    context.arc(
        PTS(servo_holder_right - CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_bottom - CORNER_ROUNDING_RADIUS),
        PTS(CORNER_ROUNDING_RADIUS),
        0,
        0.5 * math.pi
    )

    # bottom edge of servo holder
    context.line_to(
        PTS(servo_holder_left + CORNER_ROUNDING_RADIUS),
        PTS(servo_holder_bottom)
    )

    context.close_path()
    context.stroke()

    board_left = chassis_left + 0.5 * (CHASSIS_BASIC_WIDTH - BOARD_WIDTH)
    board_right = board_left + BOARD_WIDTH
    board_bottom = chassis_bottom - BOARD_CLEARANCE_WITH_BOTTOM_EDGE
    board_top = board_bottom - BOARD_BREADTH_MAX

    for (mount_x, mount_y) in BOARD_MOUNTING_HOLES:
        draw_mounting_hole(context, M3_MOUNTING_HOLE, board_left + mount_x, board_top + mount_y)

    caster_mount_bottom = caster_extrusion_bottom - (CASTER_WHEEL_EDGE_DISTANCE)
    caster_mount_top = caster_mount_bottom - CASTER_WHEEL_MOUNTING_BREADTH
    caster_mount_left = chassis_left + 0.5 * (CHASSIS_BASIC_WIDTH - CASTER_WHEEL_MOUNTING_WIDTH)
    caster_mount_right = caster_mount_left + CASTER_WHEEL_MOUNTING_WIDTH

    draw_mounting_hole(context, M3_MOUNTING_HOLE, caster_mount_left, caster_mount_top)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, caster_mount_right, caster_mount_top)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, caster_mount_left, caster_mount_bottom)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, caster_mount_right, caster_mount_bottom)

    battery_align = chassis_vcenter - 0.2 * CHASSIS_BASIC_BREADTH
    battery_left = chassis_hcenter - 0.5 * (BATTERY_WIDTH + 2 * BATTERY_HOLE_CLEARANCE)
    battery_right = battery_left + (BATTERY_WIDTH + 2 * BATTERY_HOLE_CLEARANCE)
    draw_mounting_hole(context, BATTERY_MOUNTING_HOLE, battery_left, battery_align)
    draw_mounting_hole(context, BATTERY_MOUNTING_HOLE, battery_right, battery_align)
    draw_mounting_hole(context, BATTERY_MOUNTING_HOLE, battery_left, battery_align + 20.0 * units.mm)
    draw_mounting_hole(context, BATTERY_MOUNTING_HOLE, battery_right, battery_align + 20.0 * units.mm)

    motor_left_top = chassis_top + MOTOR_MOUNTING_EDGE_CLEARANCE + 0.5 * M3_MOUNTING_HOLE.hole_diameter
    motor_left_bottom = motor_left_top + MOTOR_MOUNTING_BREADTH
    motor_left_left = chassis_left + MOTOR_MOUNTING_EDGE_CLEARANCE + 0.5 * M3_MOUNTING_HOLE.hole_diameter
    motor_left_right = motor_left_left + MOTOR_MOUNTING_WIDTH
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_left_left, motor_left_top)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_left_right, motor_left_top)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_left_left, motor_left_bottom)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_left_right, motor_left_bottom)

    battery_hole_align = 0.5 * (motor_left_top + motor_left_bottom)
    #draw_mounting_hole(context, BATTERY_CONNECTOR_HOLE, chassis_hcenter, battery_hole_align)

    motor_right_top = motor_left_top
    motor_right_bottom = motor_left_bottom
    motor_right_right = chassis_right - (MOTOR_MOUNTING_EDGE_CLEARANCE + 0.5 * M3_MOUNTING_HOLE.hole_diameter)
    motor_right_left = motor_right_right - MOTOR_MOUNTING_WIDTH
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_right_left, motor_right_top)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_right_right, motor_right_top)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_right_left, motor_right_bottom)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, motor_right_right, motor_right_bottom)

    servo_mount_hcenter = 0.5 * (left_servo_mount_left + left_servo_mount_right)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, servo_mount_hcenter, servo_mount_bottom - SERVO_MOUNT_HOLE_CLEARANCE - 0.5 * M3_MOUNTING_HOLE.nut_width)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, servo_mount_hcenter, servo_mount_top + SERVO_MOUNT_HOLE_CLEARANCE + 0.5 * M3_MOUNTING_HOLE.nut_width)

    servo_mount_hcenter = 0.5 * (right_servo_mount_left + right_servo_mount_right)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, servo_mount_hcenter, servo_mount_bottom - SERVO_MOUNT_HOLE_CLEARANCE - 0.5 * M3_MOUNTING_HOLE.nut_width)
    draw_mounting_hole(context, M3_MOUNTING_HOLE, servo_mount_hcenter, servo_mount_top + SERVO_MOUNT_HOLE_CLEARANCE + 0.5 * M3_MOUNTING_HOLE.nut_width)

    servo_holder_mounting_hole_y = 0.5 * (servo_mount_bottom + SERVO_INSET_WIDTH_MINOR + CHASSIS_THICKNESS + servo_mount_top)
    servo_holder_mounting_hole_l = servo_left_prong_right - 0.5 * SERVO_MOUNTING_SHELF_WIDTH
    servo_holder_mounting_hole_r = servo_right_prong_left + 0.5 * SERVO_MOUNTING_SHELF_WIDTH
    draw_mounting_hole(context, M2_MOUNTING_HOLE, servo_holder_mounting_hole_l, servo_holder_mounting_hole_y)
    draw_mounting_hole(context, M2_MOUNTING_HOLE, servo_holder_mounting_hole_r, servo_holder_mounting_hole_y)

    servo_holder_slot_left = right_servo_mount_left + SERVO_MOUNTING_SHELF_DEPTH
    servo_holder_slot_right = servo_holder_slot_left + CHASSIS_THICKNESS + SERVO_INSET_CLEARANCE
    servo_holder_slot_bottom_bottom = chassis_top - 1.5 * units.mm
    servo_holder_slot_bottom_top = servo_holder_slot_bottom_bottom - (SERVO_INSET_WIDTH_MINOR + SERVO_INSET_CLEARANCE)
    servo_holder_slot_top_top = servo_holder_slot_bottom_bottom - SERVO_INSET_WIDTH_MAJOR
    servo_holder_slot_top_bottom = servo_holder_slot_top_top + SERVO_INSET_WIDTH_MINOR + SERVO_INSET_CLEARANCE
    load_line_style(context, CUT_LINE_STYLE)
    draw_rect(context,
        servo_holder_slot_bottom_top, servo_holder_slot_bottom_bottom,
        servo_holder_slot_left, servo_holder_slot_right
    )
    draw_rect(context,
        servo_holder_slot_top_top, servo_holder_slot_top_bottom,
        servo_holder_slot_left, servo_holder_slot_right
    )

    servo_holder_slot_right = left_servo_mount_right - SERVO_MOUNTING_SHELF_DEPTH
    servo_holder_slot_left = servo_holder_slot_right - (CHASSIS_THICKNESS + SERVO_INSET_CLEARANCE)
    draw_rect(context,
        servo_holder_slot_bottom_top, servo_holder_slot_bottom_bottom,
        servo_holder_slot_left, servo_holder_slot_right
    )
    draw_rect(context,
        servo_holder_slot_top_top, servo_holder_slot_top_bottom,
        servo_holder_slot_left, servo_holder_slot_right
    )


    context.move_to(
        PTS(servo_holder_slot_left),
        PTS(servo_holder_slot_top_bottom)
    )
    context.line_to(
        PTS(servo_holder_slot_left),
        PTS(servo_holder_slot_top_top)
    )
    context.line_to(
        PTS(servo_holder_slot_right),
        PTS(servo_holder_slot_top_top)
    )
    context.line_to(
        PTS(servo_holder_slot_right),
        PTS(servo_holder_slot_top_bottom)
    )
    context.line_to(
        PTS(servo_holder_slot_left),
        PTS(servo_holder_slot_top_bottom)
    )
    load_line_style(context, CUT_LINE_STYLE)
    context.close_path()
    context.stroke()

    if BOARD_OUTLINE:
        context.move_to(
            PTS(board_left),
            PTS(board_top)
        )
        context.line_to(
            PTS(board_right),
            PTS(board_top)
        )
        context.line_to(
            PTS(board_right),
            PTS(board_top + BOARD_BREADTH_MIN)
        )
        context.rel_line_to(
            -PTS(BOARD_RECESSED_LONG_SEGMENT),
            0
        )
        context.rel_line_to(
            -PTS(math.cos(0.25 * math.pi) * BOARD_ANGLED_SEGMENT),
            PTS(math.sin(0.25 * math.pi) * BOARD_ANGLED_SEGMENT)
        )
        context.rel_line_to(
            -PTS(BOARD_EXTENDED_SEGMENT),
            0
        )
        context.rel_line_to(
            -PTS(math.cos(0.25 * math.pi) * BOARD_ANGLED_SEGMENT),
            -PTS(math.sin(0.25 * math.pi) * BOARD_ANGLED_SEGMENT)
        )
        context.rel_line_to(
            -PTS(BOARD_RECESSED_SHORT_SEGMENT),
            0
        )
        context.line_to(
            PTS(board_left),
            PTS(board_top)
        )
        load_line_style(context, BOARD_OUTLINE_STYLE)
        context.stroke()

    # load_line_style(context, MOUNTING_HOLE_GUIDE_STYLE)
    # context.move_to(
    #     PTS(chassis_hcenter),
    #     0
    # )
    # context.line_to(
    #     PTS(chassis_hcenter),
    #     PTS(CANVAS_HEIGHT)
    # )
    context.stroke()

    context.restore()

if __name__ == '__main__':
    if TESSELATION:
        w = TESSELATION_CANVAS_WIDTH.to(units.points).magnitude
        h = TESSELATION_CANVAS_HEIGHT.to(units.points).magnitude
        count_h = TESSELATION_COUNT_H
        count_v = TESSELATION_COUNT_V
    else:
        w = PTS(CANVAS_WIDTH)
        h = PTS(CANVAS_HEIGHT)
        count_h = 1
        count_v = 1
    with cairo.SVGSurface("chassis.svg", w, h) as surface:
        context = cairo.Context(surface)
        for y in range(count_v):
            for x in range(count_h):
                context.identity_matrix()
                context.translate(
                    (x * TESSELATION_OFFSET_X).to(units.points).magnitude,
                    (y * TESSELATION_OFFSET_Y).to(units.points).magnitude
                )
                render(context)
