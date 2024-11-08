############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

from typing import List

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)


class MG_LINE(object):
    
    @staticmethod
    def slope_constant( p1: tuple, p2: tuple ):
        '''
            Expected Input
                p1      : ( x, y )  --> ( a, b )
                p2      : ( x, y )  --> ( c, d )
                
            Expected Output
                (float, float)  : ( slope, constant ) about stright-line.
                    slope       : slope value (A: Ax + B = y)
                    constant    : additional constant value (B: Ax + B = y)
        '''
        try:
            if p1 is None or p2 is None:
                raise RuntimeError(f"Invalid Arguments: 'point1'({p1}) or 'point2'({p2}) is NULL.")

            denominator = float(p1[0] - p2[0])
            if denominator == 0.0:
                raise RuntimeError(f"Invalid Arguments: 'point1.x' and 'point2.x' have to be not equal. (Can not divide)")
            
            slope = float(p1[1] - p2[1])/denominator                    # (b-d) / (a-c)
            constant = float(p1[0]*p2[1] - p1[1]*p2[0])/denominator     # (ad-bc) / (a-c)
            return (slope, constant)
        
        except BaseException as e:
            logger.error(e)
            raise e
        
    @staticmethod
    def intersection_point( line1: tuple, line2: tuple ):
        '''
            Expected Input
                line1       : ( slope, constant )       --> ( A, B )
                line2       : ( slope, constant )       --> ( C, D )
                
            Expected output
                (float, float)      : ( x, y ) about intersected point.
        '''
        try:
            if line1 is None or line2 is None:
                raise RuntimeError(f"Invalid Arguments: 'line1'({line1}) or 'line2'({line2}) is NULL.")
            
            denominator = float(line1[0] - line2[0])
            if denominator == 0.0:
                raise RuntimeError(f"Invalid Arguments: 'line1.slope' and 'line2.slope' have to be not equal. (Can not divide)")
                
            px = float(line2[1]- line1[1])/denominator                       # (D-B) / (A-C)
            py = float(line1[0]*line2[1] - line1[1]*line2[0])/denominator    # (AD-BC) / (A-C)
            return (px, py)
        
        except BaseException as e:
            logger.error(e)
            raise e



class MG_RECT(object):
    class MERGE_COND:
        EQ_LEFT = "E-Left"
        EQ_RIGHT = "E-Right"
    
    @staticmethod
    def check_validation(target: str, rect: list):
        try:
            if rect is None:
                raise RuntimeError(f"Invalid Arguments: '{target}' Rectangle-Data is NULL.")
            
            if len(rect) != 4:
                raise RuntimeError(f"Invalid Arguments: '{target}' Rectangle-Data's length is not 4. ({rect})")
            
            if rect[0] < 0 or rect[1] < 0 or rect[2] <= 0 or rect[3] <= 0:
                raise RuntimeError(f"Invalid Arguments: '{target}' Rectangle-Data is invalid scope. ({rect})")

        except BaseException as e:
            logger.error(e)
            raise e

    @staticmethod
    def distinguish_intersected(src_rect: list, rect2: list):
        '''
            Expected Input
                src_rect: [left, top, width, height]
                rect2   : [left, top, width, height]
            
            Expected Output
                list, list    : 1. Not intersected area(rectangle) in 'src_rect' against about 'rect2'
                                   Format [left, top, width, height]
                                   Valid-value : rect , None
                                2. Pure intersected area(rectangle) in 'src_rect' with 'rect2'
                                   Format [left, top, width, height]
                                   Valid-value : rect , None
        '''
        def find_max_not_intersected_area(parent: list, inner: list):
            return MG_RECT.max_area([
                [parent[0], parent[1], inner[0]-parent[0], parent[3]],
                [parent[0], parent[1], parent[2], inner[1]-parent[1]],
                [inner[0]+inner[2], parent[1], parent[0]+parent[2]-inner[0]-inner[2], parent[3]],
                [parent[0], inner[1]+inner[3], parent[2], parent[1]+parent[3]-inner[1]-inner[3]]
            ])
            
        try:
            # check validation
            MG_RECT.check_validation('src_rect', src_rect)
            MG_RECT.check_validation('rect2', rect2)

            # calculate intersection coordinate.
            intersect = MG_RECT.calc_intersection(src_rect, rect2)
            if intersect is None:
                return src_rect, None       # not intersected case.
            
            # calculate biggest not-intersected coordinate.
            max_rect = find_max_not_intersected_area(src_rect, intersect)
            return max_rect, intersect      # intersected case.
            
        except BaseException as e:
            logger.error(e)
            raise e

    @staticmethod
    def calc_intersection(rect1: list, rect2: list):
        try:
            # check validation
            MG_RECT.check_validation('rect1', rect1)
            MG_RECT.check_validation('rect2', rect2)
            
            # calculate
            left = max(rect1[0], rect2[0])
            top = max(rect1[1], rect2[1])
            width = min(rect1[0]+rect1[2], rect2[0]+rect2[2]) - left
            height = min(rect1[1]+rect1[3], rect2[1]+rect2[3]) - top
            
            # check validation
            if width <= 0 or height <= 0:
                return None
            
            return [left, top, width, height]
        except BaseException as e:
            logger.error(e)
            raise e

    @staticmethod
    def is_intersection(rec1: list, rec2: list):
        '''
            Expected Input
                rec1    : [left, top, width, height]
                rec2    : [left, top, width, height]
            
            Expected Output
                boolean : If there is intersected region, then True. Other case is False.
        '''
        
        try:
            # check validation
            MG_RECT.check_validation( 'rec1', rec1 )
            MG_RECT.check_validation( 'rec2', rec2 )
            
            # make variables
            rec1_end_x = rec1[0] + rec1[2]
            rec1_end_y = rec1[1] + rec1[3]
            rec2_end_x = rec2[0] + rec2[2]
            rec2_end_y = rec2[1] + rec2[3]
            
            # Compare rec1's edge-pointer and rec2's edge-pointer.
            if MG_RECT.is_inner_point( rec1, (rec2[0]   , rec2[1])    ) is True or \
               MG_RECT.is_inner_point( rec1, (rec2_end_x, rec2[1])    ) is True or \
               MG_RECT.is_inner_point( rec1, (rec2[0]   , rec2_end_y) ) is True or \
               MG_RECT.is_inner_point( rec1, (rec2_end_x, rec2_end_y) ) is True or \
               MG_RECT.is_inner_point( rec2, (rec1[0]   , rec1[1])    ) is True or \
               MG_RECT.is_inner_point( rec2, (rec1_end_x, rec1[1])    ) is True or \
               MG_RECT.is_inner_point( rec2, (rec1[0]   , rec1_end_y) ) is True or \
               MG_RECT.is_inner_point( rec2, (rec1_end_x, rec1_end_y) ) is True:
                return True
            
            # Extract intersection_point between rec1's diagonal-line and rec2'c other diagonal-line.
            rec1_diagL = MG_LINE.slope_constant( (rec1[0], rec1[1]), (rec1_end_x, rec1_end_y) )
            rec2_diagL = MG_LINE.slope_constant( (rec2[0], rec2_end_y), (rec2_end_x, rec2[1]) )
            intersectP = MG_LINE.intersection_point( rec1_diagL, rec2_diagL )
            
            # Check intersection_point
            if MG_RECT.is_inner_point( rec1, intersectP ) is True and MG_RECT.is_inner_point( rec2, intersectP ) is True:
                return True
            
            return False
        except BaseException as e:
            logger.error(e)
            raise e
        
    @staticmethod
    def is_inner_point(rect: list, point: tuple):
        '''
            Expected Input
                rect        : [ left(x), top(y), width, height ]
                point       : ( x, y )
            
            Expected Output
                boolean     : If there is 'point' in 'rect', then True. Otherwise False.
        '''
        try:
            MG_RECT.check_validation( 'rect', rect )
            
            if float(rect[0]) >= float(point[0]) or float(point[0]) >= float(rect[0]+rect[2]):
                return False
            if float(rect[1]) >= float(point[1]) or float(point[1]) >= float(rect[1]+rect[3]):
                return False
            return True
        
        except BaseException as e:
            logger.error(e)
            raise e
    
    @staticmethod
    def is_include(parent: list, child: list):
        '''
            Expected Input
                - parent    : [left, top, width, height]
                - child     : [left, top, width, height]
        '''
        try:
            MG_RECT.check_validation( 'parent', parent )
            MG_RECT.check_validation( 'child', child )
            
            if parent[0] > child[0] or child[0] >= parent[0] + parent[2]:
                return False
            if parent[1] > child[1] or child[1] >= parent[1] + parent[3]:
                return False
            if child[0] + child[2] > parent[0] + parent[2]:
                return False
            if child[1] + child[3] > parent[1] + parent[3]:
                return False
            
            return True
        except BaseException as e:
            logger.error(e)
            raise e

    @staticmethod
    def max_area(rect_list: list):
        '''
            Expected Input
                rect_list   : [ [left, top, width, height], [left, top, width, height], ... ]
        '''
        def calc_area(item: list):
            return item[2]*item[3]
        
        try:
            if rect_list is None:
                raise RuntimeError("rect_list is NULL.")
            
            max_res = None
            for rect in rect_list:
                if max_res is None or calc_area(max_res) < calc_area(rect):
                    max_res = rect
                    
            return max_res if calc_area(max_res) > 0 else None
        except BaseException as e:
            logger.error(e)
            raise e

    @staticmethod
    def merge_area(src: list, dest: list, cond: List[MERGE_COND] =list()):
        '''
            Expected Input
                src     : [left, top, width, height]
                dest    : [left, top, width, height]
                cond    : [str]     Valid-Values [ E-Left, E-Right, None ]
        '''
        try:
            res = None
            if src is None or dest is None:
                raise RuntimeError(f"src({src}) or dest({dest}) is None.")
            
            for item in cond:
                if item == MG_RECT.MERGE_COND.EQ_LEFT:
                    if src[0] != dest[0]:
                        res = src
                        break
                if item == MG_RECT.MERGE_COND.EQ_RIGHT:
                    if src[0] + src[2] != dest[0] + dest[2]:
                        res = src
                        break
            
            if res is None:
                res = [0, 0, 0, 0]
                res[0] = min(src[0], dest[0])
                res[1] = min(src[1], dest[1])
                res[2] = max(src[0]+src[2], dest[0]+dest[2]) - res[0]
                res[3] = max(src[1]+src[3], dest[1]+dest[3]) - res[1]
            
            return res
        except BaseException as e:
            logger.error(e)
            raise e
