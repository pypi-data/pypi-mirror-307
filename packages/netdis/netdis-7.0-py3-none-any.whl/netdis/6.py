import multiprocessing


def child_process(pipe):
    message_from_parent = pipe.recv()
    print(f"Child received message: {message_from_parent}")
    response = "Hello, Parent! This is Child."
    pipe.send(response)

def parent_process(pipe):
    pipe.send("Hello, Child! This is Parent.")
    response = pipe.recv()
    print(f"Parent received response: {response}")

if __name__ == '__main__':
    parent_pipe, child_pipe = multiprocessing.Pipe()

    parent_proc = multiprocessing.Process(target=parent_process, args=(parent_pipe,))
    child_proc = multiprocessing.Process(target=child_process, args=(child_pipe,))

    parent_proc.start()
    child_proc.start()

    parent_proc.join()
    child_proc.join()
