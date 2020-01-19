def join_params(old_params, new_params):
  new_dict = dict(list(old_params.items()) + list(new_params.items()))

  return new_dict
