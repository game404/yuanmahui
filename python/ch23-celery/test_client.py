from myapp import add, app

# app.conf.update(
#
# )

# app.log.setup("DEBUG", redirect_stdouts=True)

task = add.delay(16, 16)

print(task)
print(task.get())
