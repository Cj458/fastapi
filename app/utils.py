import os
from reportlab.pdfgen import canvas
from passlib.context import CryptContext

pwd_contex = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_contex.hash(password)

def generate_pdf_report(user_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"{user_data['id']}-{user_data['first_name']}-report.pdf"
    file_path = os.path.join(output_dir, file_name)

    pdf = canvas.Canvas(file_path)


    # User Information
    pdf.drawString(100, 750, f"User Report for {user_data['first_name']} {user_data['last_name']}")
    pdf.drawString(100, 730, f"User ID: {user_data['id']}")
    pdf.drawString(100, 710, f"City: {user_data['city']}")
    pdf.drawString(100, 690, f"Country: {user_data['country']}")
    pdf.drawString(100, 670, "-" * 40)

    # Followers Information
    if 'followers' in user_data:
        pdf.drawString(100, 650, "Followers:")
        y_position = 630
        for follower in user_data['followers']:
            pdf.drawString(120, y_position, f"{follower['first_name']} {follower['last_name']} (ID: {follower['id']})")
            y_position -= 20
        pdf.drawString(100, y_position, "-" * 40)

    # Groups Information
    if 'groups' in user_data:
        pdf.drawString(100, y_position - 20, "Groups:")
        y_position -= 40

        for group_name in user_data['groups']:
            if y_position < 20:
                pdf.showPage()
                y_position = 780

            pdf.drawString(120, y_position, group_name)
            y_position -= 20

    pdf.showPage()
    pdf.save()

    return file_path

