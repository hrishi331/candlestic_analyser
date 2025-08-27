from pushbullet import Pushbullet

pb = Pushbullet("o.QGYQN73kbVFUOHG7BAfa3onk5gbF0UjC")
push = pb.push_note("Hello", "How are you!")
print("Notification sent!")