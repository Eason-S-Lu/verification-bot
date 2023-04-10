import discord
import random
import smtplib, ssl

# Set up the Discord client
client = discord.Client()

# Define the email settings
smtp_server = "smtp.gmail.com"
port = 465  # For SSL
sender_email = "your_email@example.com"  # Enter your address
password = "your_password"  # Enter your password

# Define the verification code generator
def generate_verification_code():
    return str(random.randint(100000, 999999))

# Define the email sender function
def send_verification_code(recipient_email, verification_code):
    message = """\
    Subject: Verification Code

    Your verification code is: """ + verification_code

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message)

# Define the on_message event handler
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!verify'):
        # Ask the user for their email address
        await message.channel.send("Please enter your email address:")
        email = await client.wait_for('message', check=lambda m: m.author == message.author)
        
        # Generate and send the verification code
        verification_code = generate_verification_code()
        send_verification_code(email.content, verification_code)
        await message.channel.send("A verification code has been sent to your email address.")
        
        # Ask the user for the verification code
        await message.channel.send("Please enter the verification code:")
        code = await client.wait_for('message', check=lambda m: m.author == message.author)
        
        # Check if the verification code matches
        if code.content == verification_code:
            # Grant the user the verified role
            role = discord.utils.get(message.guild.roles, name="verified")
            await message.author.add_roles(role)
            await message.channel.send("You have been verified!")
        else:
            await message.channel.send("The verification code you entered is invalid.")
            
# Run the Discord client
client.run('your_bot_token')