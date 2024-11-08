from multiprocessing import Process, Queue

def sender(queue):
    message = "Hello from Process 1!"
    queue.put(message)
    print("Process 1: Message sent to the queue.")

def receiver(queue):
    message = queue.get()
    print(f"Process 2: Message received from queue: {message}")

if __name__ == "__main__":
    queue = Queue()

    process1 = Process(target=sender, args=(queue,))
    process2 = Process(target=receiver, args=(queue,))

    process1.start()
    process1.join()  

    process2.start()
    process2.join()
