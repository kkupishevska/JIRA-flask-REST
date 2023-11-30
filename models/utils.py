class UtilsClass:
  def update_attributes(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)