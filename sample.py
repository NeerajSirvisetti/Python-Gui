import time
class ContinuousChecker:
  def __init__(self):
      self.is_running = False

  def start_continuous_check(self):
      self.is_running = True
      while self.is_running:
          # Your continuous checking logic goes here
          print("Continuous checking...")
          time.sleep(1)

  def stop_continuous_check(self):
      self.is_running = False


class AnotherClass:
  def __init__(self):
      self.checker_instance = ContinuousChecker()

  def start_continuous_checking_from_another_class(self):
      self.checker_instance.start_continuous_check()

  def stop_continuous_checking_from_another_class(self):
      self.checker_instance.stop_continuous_check()


# Example usage
if __name__ == "__main__":
  another_instance = AnotherClass()
  another_instance.start_continuous_checking_from_another_class()

  try:
      # Allow the continuous check to run for a while
      time.sleep(5)
  finally:
      # Stop the continuous check when done
      another_instance.stop_continuous_checking_from_another_class()
