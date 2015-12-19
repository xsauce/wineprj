from handler.CommonHandler import CommonHandler
from utils.verification_code import gen_code

__author__ = 'sam'

VALCODE_NAME = 'vcode'

class VerificationCodeHandler(CommonHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        code, image_bytes = gen_code()
        if not self.session:
            self.create_session_and_set_item(VALCODE_NAME, code)
        else:
            self.session.set_item(VALCODE_NAME, code)
        self.write(image_bytes)
        self.flush()
        self.finish()


