from base_test_ci import BaseTest
import unittest

class Test0(BaseTest):
    def test_verifyUp(self):
        self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        for i in range(0, self.testLen):
            if self.endFlag:
                self.assertEqual(b'UP', self.message)
                return
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()