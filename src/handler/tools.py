from handler.CommonHandler import CommonHandler
from utils.verification_code import gen_code

__author__ = 'sam'

class VerificationCodeHandler(CommonHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        code, image_bytes = gen_code()
        self.create_session_and_set_item('vcode', code)
        self.write(image_bytes)
        self.flush()
        self.finish()


