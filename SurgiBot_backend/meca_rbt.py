import mecademicpy.robot as mdr
import numpy as np

ip = "192.168.0.100:10000"

class mecaRbt(object):
    _shared_borg_state = {} # store share variable
    
    def __init__(self, *args, **kwargs) -> None:
        print("[mecaRbt]: initiating robot")
        self.robot = mdr.Robot()

        if "ip" in kwargs.keys():
            self.ip = ip
        pass
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(mecaRbt, cls).__new__(cls)
            cls.instance.__dict__ = cls._shared_borg_state
        return cls.instance
    
    def connect(self):
        print("[mecaRbt]: connecting")
        try:
            self.robot.Connect(address=self.ip)
            print('[mecaRbt]: Connected to robot')
            return True
        except Exception as e:
            print(f'[mecaRbt]: Robot failed to connect. Is the IP address correct? {e}')
        
        return False
    
    def disconnect(self):
        print("[mecaRbt]: disconnecting")
        if (self.robot.IsConnected()):
            self.robot.Disconnect()
        print("[mecaRbt]: disconnected")
        
    
    def moveRbtJoints(self, jointVel, joints):
        # --- try to connect the robot
        if (self.connect()):
        # --------------main function begins--------------
            try:
                self.robot.ActivateRobot()
                self.robot.SetJointVel(jointVel)
                self.robot.MoveJoints(joints[0],
                                    joints[1],
                                    joints[2],
                                    joints[3],
                                    joints[4],
                                    joints[5])
                self.robot.WaitIdle(30)
            # --------------main function ends--------------
            
            except Exception as exception:
                if self.robot.GetStatusRobot().error_status:
                    print(exception)
                    print('Robot has encountered an error, attempting to clear...')
                    self.robot.ResetError()
                    self.robot.ResumeMotion()
                else:
                    raise

            # --- release the connection resource
            self.disconnect()

    def moveRbtPose(self, jointVel, pose):
        if (self.connect()):
            try:
                self.robot.ActivateRobot()
                self.robot.SetJointVel(jointVel)
                # Send motion commands to have the robot draw out a square.
                self.robot.MovePose(pose[0],
                            pose[1],
                            pose[2],
                            pose[3],
                            pose[4],
                            pose[5])
                # Wait until checkpoint is reached. Without this wait, the script would immediately
                # reach the DeactivateRobot and Disconnect command, which stops the motion.
                self.robot.WaitIdle(30)

            except Exception as exception:
                    # Attempt to clear error if robot is in error.
                    if self.robot.GetStatusRobot().error_status:
                        print(exception)
                        print('Robot has encountered an error, attempting to clear...')
                        self.robot.ResetError()
                        self.robot.ResumeMotion()
                    else:
                        raise
            self.disconnect()
    
    def jogRbt(self, jointVel, jog_dir, jog_step):
        if (self.connect()):
            try:
                self.robot.ActivateRobot()
                self.robot.SetJointVel(jointVel)
                if (jog_dir == 'Z+'):
                    self.robot.MoveLinRelWrf(0, 0, jog_step, 0, 0, 0)
                elif (jog_dir == 'Z-'):
                    self.robot.MoveLinRelWrf(0, 0, -jog_step, 0, 0, 0)
                elif (jog_dir == 'X+'):
                    self.robot.MoveLinRelWrf(jog_step, 0, 0, 0, 0, 0)
                elif (jog_dir == 'X-'):
                    self.robot.MoveLinRelWrf(-jog_step, 0, 0, 0, 0, 0)
                elif (jog_dir == 'Y+'):
                    self.robot.MoveLinRelWrf(0, -jog_step, 0, 0, 0, 0)
                elif (jog_dir == 'Y-'):
                    self.robot.MoveLinRelWrf(0, +jog_step, 0, 0, 0, 0)
                # Send motion commands to have the robot draw out a square.

                # Wait until checkpoint is reached. Without this wait, the script would immediately
                # reach the DeactivateRobot and Disconnect command, which stops the motion.
                self.robot.WaitIdle(30)

            except Exception as exception:
                    # Attempt to clear error if robot is in error.
                    if self.robot.GetStatusRobot().error_status:
                        print(exception)
                        print('Robot has encountered an error, attempting to clear...')
                        self.robot.ResetError()
                        self.robot.ResumeMotion()
                    else:
                        raise

            self.disconnect()


    def getJoints(self):
        if (self.connect()):
            flag = 1
            cnt = 0
            while flag:
                jointlist =  self.robot.GetRtTargetJointPos()
                jointlist_np = np.array(jointlist)
                if not np.all(jointlist_np == 0.0):
                    print(jointlist)
                    return jointlist
                cnt += 1
                if (cnt >= 100):
                    flag = 0
    
    def rbtDeactivate(self):
        if (self.connect()):
            try:
                self.robot.DeactivateRobot()

            except Exception as exception:
                # Attempt to clear error if robot is in error.
                if self.robot.GetStatusRobot().error_status:
                    print(exception)
                    print('Robot has encountered an error, attempting to clear...')
                    self.robot.ResetError()
                    self.robot.ResumeMotion()
                else:
                    raise
            
            self.disconnect()


    def __del__(self):
        if (self.robot.IsConnected()):
            self.disconnect()

    

if __name__ == "__main__":
    pass