############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import cv2
from . import lib_path as lpath
from . import lib_time as ltime
from .lib_thread import CThread

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(mode=CmyLogger.DEBUG_MODE)

__all__ = ["CamRecoder"]


class CamRecoder(object):
    
    _m_cam_ = None
    _m_out_: cv2.VideoWriter = None
    _m_mirror_: bool = False
    _m_delay_: int = -1
    _m_thread_: CThread = None
    _m_func_uptime_ = None
    
    @property
    def cam(self):
        if self._m_cam_ is None:
            raise ModuleNotFoundError("'CAM' instance is None.")
        return self._m_cam_
    
    @property
    def output(self):
        if self._m_out_ is None:
            raise FileNotFoundError("'Output File' not set.")
        return self._m_out_
    
    @property
    def is_running(self):
        try:
            if self._m_thread_ is None or self._m_thread_.is_continue is False:
                return False
            return True
        except BaseException as e:
            logger.error(e)
            raise e
    
    def start(self):
        try:
            if self._m_thread_ is None:
                raise RuntimeError("Can not start Video-Thread.")
            
            # start thread
            self._m_thread_.start()
        except BaseException as e:
            logger.error(e)
            raise e
        
    def stop(self):
        try:
            self._cam_quit_()
        except BaseException as e:
            logger.error(e)
            raise e

    #############################################
    # Private Function Definition.
    ############
    def __init__(self, cam_idx: int, dir_path: str, file_name: str, mirror: bool = False, func_uptime = None):
        print()
        print("====================== CamRecoder.constructor ======================")
        logger.info(f" >>> cam_idx  : {cam_idx}")
        logger.info(f" >>> dir_path : {dir_path}")
        logger.info(f" >>> file_name: {file_name}")
        logger.info(f" >>> mirror   : {mirror}")
        print("====================================================================")

        try:
            self.__clean__()
            dir_path = lpath.get_abspath(dir_path)
            file_path = lpath.join_paths( dir_path, file_name) + ".mp4"
            lpath.make_dirs( dir_path )
            
            # set Variables.
            self._m_cam_, self._m_out_ = self._cam_init_(cam_idx, file_path)
            self._m_mirror_ = mirror
            self._m_func_uptime_ = func_uptime
            
            # check cam-operation
            self._cam_capture_(None)
            
            # create thread but not start yet.
            self._create_thread_()
        except BaseException as e:
            logger.error(e)
            raise e
    
    def __del__(self):
        self._cam_quit_()
        self.__clean__()
    
    def __clean__(self):
        self._m_cam_ = None
        self._m_out_ = None
        self._m_mirror_ = False
        self._m_delay_ = -1
        self._m_func_uptime_ = None
    
    def _cam_init_(self, cam_idx: int, file_path: str):
        try:
            if cam_idx is None or file_path is None:
                raise RuntimeError(f"Invalid Arguments. (cam_idx={cam_idx}, file_path={file_path})")
            
            # open Video module. (Ubuntu: /dev/video{X})
            cam = cv2.VideoCapture(cam_idx)
            if cam.isOpened() is False:
                raise RuntimeError(f"Can not open VideoCapture({cam_idx})")
            
            width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cam.get(cv2.CAP_PROP_FPS)
            
            # enable video-writer
            codec = cv2.VideoWriter_fourcc(*'DIVX')     # DIVX, XVID, MJPG, FMP4
            writer = cv2.VideoWriter(file_path, codec, fps, (width, height))
            if writer.isOpened() is False:
                raise RuntimeError(f"Can not enable VideoWriter({file_path}, {codec}, {fps}, ({width},{height}))")

            self._m_delay_ = round(1000/fps)
            return cam, writer
        except BaseException as e:
            logger.error(e)
            raise e
    
    def _cam_quit_(self):
        try:
            # stop thread.
            self._destroy_thread_()
            
            # close the already opened camera
            if self.cam.isOpened() is True and self.output.isOpened() is True:
                self.cam.release()
                self.output.release()       # close the already opened file
                cv2.destroyAllWindows()     # close the window and de-allocate any associated memory usage
        except (FileNotFoundError, ModuleNotFoundError) as e:
            logger.warn(e)
        except BaseException as e:
            logger.error(e)
            raise e

    def _cam_capture_(self, frame_pretime: float=None):
        try:
            # capture frame.
            while True:
                ret_val, frame = self.cam.read()           # Y:X = 480:640 , RGB type.
                if ret_val is False:
                    raise RuntimeError("Can not read image-data.")
                
                frame_time = self.cam.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                
                if frame_pretime is None or frame_time > frame_pretime:
                    break;
            
            # make UTC time of frame-measurement
            cur_time = ltime.get_UTC()
            frame_ms = float(frame_time - int(frame_time))
            if (cur_time - int(cur_time)) < frame_ms - 0.7:       # if seconds-unit is over steped, then proc - 1.0
                cur_time -= 1.0
            measured_utc = float(int(cur_time)) + frame_ms

            # convert frame by X-axis mirroring
            if self._m_mirror_ is True:
                frame = cv2.flip(frame, 1)
                
            return frame, frame_time, ltime.cvt_utc(measured_utc, date_format="%Y-%m-%d %H:%M:%S.%f")
        except BaseException as e:
            logger.error(e)
            raise e

    def _draw_timestamp_(self, frame, width: int, height: int, size: int, 
                        timestamp: str=None, uptime: float=None):
        def draw( text: str, w: int, h: int ):
            cv2.putText(frame, text=text, org=(w, h), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=size, 
                        color=(50, 0, 255), thickness=1, lineType=cv2.LINE_AA)
        try:
            if timestamp is None:
                timestamp = ltime.get_DATE()
                
            # draw 'timestamp' & 'uptime'
            draw("Time: " + timestamp, width, height)
            if uptime is not None:
                draw("Uptime: " + str(uptime), width, height + 20 * size)

            return frame
        except BaseException as e:
            logger.error(e)
            raise e
        
    ####################################
    # Thread related Private-Functions.
    ######
    def _create_thread_(self):
        try:
            if self._m_thread_ is not None:
                raise RuntimeError("Already, LogCollector-Thread is created.")
            
            self._m_thread_ = CThread("Video-thread", self._routine_thread_, daemon=True)
        except BaseException as e:
            logger.error(e)
            raise e

    def _destroy_thread_(self):
        try:
            if self.is_running is False:
                return 
            
            if self._m_thread_.is_alive() is True:
                logger.info("Try to destory LogCollector-thread.")
                self._m_thread_.is_continue = False
                self._m_thread_.join(timeout=3.0)      # Blocking Function
                
            del self._m_thread_
            self._m_thread_ = None
        except BaseException as e:
            logger.error(e)
            raise e

    def _routine_thread_(self, thr_inst: CThread):
        try:
            uptime: float = None
            logger.info( "Start Thread: {}".format(thr_inst.getName()) )

            # Thread Main-routine.
            measure_time: float = None
            while( thr_inst.is_continue ):
                try:
                    # read image from webcam.
                    frame, measure_time, timestamp = self._cam_capture_(measure_time)
                    if self._m_func_uptime_ is not None:
                        uptime = self._m_func_uptime_()
                    
                    # set timestamp & uptime
                    frame = self._draw_timestamp_(frame, width=20, height=420, size=2, 
                                                  timestamp=timestamp, uptime=uptime)
                    
                    # show & save frame-data to viewer & file.
                    cv2.imshow('CAM Viewer', frame)
                    self.output.write(frame)
                    
                    # wait next frame.
                    cv2.waitKey(self._m_delay_)
                except BaseException as e:
                    logger.error(e)
                    # raise e
                
            # Terminate thread.
            thr_inst.is_continue = False
            
        except BaseException as e:
            logger.error(e)
            
        logger.info("Destroyed Video-Thread.")
        return 0;
