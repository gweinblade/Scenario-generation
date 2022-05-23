import gpt_2_simple as gpt2

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)



gpt2.generate(sess,
              length=100,
              temperature=0.7,
              prefix="You are on a quest to defeat the evil dragon of Larion. You've heard he lives up at the north of the kingdom. You set on the path to defeat him and walk into a dark forest. As you enter the forest you see",
              truncate='<|endoftext|>',
              include_prefix=True,
              nsamples=20,
              batch_size=20
              )