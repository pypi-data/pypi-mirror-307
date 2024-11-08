import multiprocessing as mp
import ctypes


def shared_memory():
    return mp.Array(ctypes.c_char, b" " * 50) 

def process_write(shared_data):
    try:
        with shared_data.get_lock():
            message = b"Hello from Process 1!"
            shared_data[:len(message)] = message 
            print("Value written to shared memory:", message.decode())
    except Exception as e:
        print(f"Error in Process 1: {e}")

def process_read(shared_data):
    try:
        with shared_data.get_lock():
            print("Value read from shared memory:", shared_data.value.decode().rstrip())
    except Exception as e:
        print(f"Error in Process 2: {e}")

if __name__ == '__main__':

    shared_data = shared_memory()

    p1 = mp.Process(target=process_write, args=(shared_data,))
    p1.start()
    p1.join() 

    p2 = mp.Process(target=process_read, args=(shared_data,))
    p2.start()
    p2.join() 

    print("Both processes have finished.")
