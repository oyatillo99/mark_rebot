def decor(func):

  def wrapper(user_id,is_new=False, **kwarg):
    print(is_new)

    func(user_id, **kwarg)

      
  return wrapper

@decor
def one(user_id, **kwarg):
  print(user_id)
  print(kwarg)





@decor
def two(user_id):
  print(user_id)
  

one(4,lol = 5)
two(5, is_new=True)



      
