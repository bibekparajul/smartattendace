import dlib
import numpy as np
import cv2
import os
import pandas as pd
import time
import logging
import sqlite3
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client


# Dlib  / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib landmark / Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# Create a connection to the database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create a table for the current date
current_date = datetime.datetime.now().strftime("%Y_%m_%d")  # Replace hyphens with underscores
table_name = "attendance"
create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (name TEXT, time TEXT, date DATE, UNIQUE(name, date))"
cursor.execute(create_table_sql)

# Commit changes and close the connection
conn.commit()
conn.close()


class Face_Recognizer:
    def __init__(self):
        self.font = cv2.FONT_ITALIC

        # Email configuration
        self.email_sender = 'trafficfine11@gmail.com'
        self.email_password = 'etdytbbrihvhkzbo'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        # FPS
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        # cnt for frame
        self.frame_cnt = 0

        #  Save the features of faces in the database
        self.face_features_known_list = []
        # / Save the name of faces in the database
        self.face_name_known_list = []
        self.face_email_known_list = []

        #  List to save centroid positions of ROI in frame N-1 and N
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        # List to save names of objects in frame N-1 and N
        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []

        #  cnt for faces in frame N-1 and N
        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        # Save the e-distance for faceX when recognizing
        self.current_frame_face_X_similarity_list = []

        # Save the positions and names of current faces captured
        self.current_frame_face_position_list = []
        #  Save the features of people in current frame
        self.current_frame_face_feature_list = []

        # Similarity threshold
        self.similarity_threshold = 0.93
        # List to keep track of absent students
        self.absent_students = []

    #  "features_all.csv"  / Get known faces from "features.all.csv"

    absent_students = []

    # def send_email_notification(self):
    #     if self.absent_students:
    #         subject = "Attendance Notification"
    #         body = "Dear Parent,\n\nYour child was present today."
    #
    #         msg = MIMEMultipart()
    #         msg['From'] = self.email_sender
    #         msg['To'] = ', '.join(self.absent_students)
    #         msg['Subject'] = subject
    #         msg.attach(MIMEText(body, 'plain'))
    #
    #         try:
    #             server = smtplib.SMTP(self.smtp_server, self.smtp_port)
    #             server.starttls()
    #             server.login(self.email_sender, self.email_password)
    #             text = msg.as_string()
    #             server.sendmail(self.email_sender, self.absent_students, text)
    #             server.quit()
    #             logging.info("Email notification sent to present students.")
    #         except Exception as e:
    #             logging.error(f"Failed to send email notification. Error: {str(e)}")

    # def send_email_notification(self):
    #     if self.absent_students:
    #         subject = "Attendance Notification"
    #         body = "Dear Parent,\n\nYour child was present today."
    #
    #         # Map names to email addresses
    #         absent_students_emails = [self.face_email_known_list[self.face_name_known_list.index(name)] for name in
    #                                   self.absent_students]
    #
    #         msg = MIMEMultipart()
    #         msg['From'] = self.email_sender
    #         msg['To'] = ', '.join(absent_students_emails)
    #         msg['Subject'] = subject
    #         msg.attach(MIMEText(body, 'plain'))
    #
    #         try:
    #             server = smtplib.SMTP(self.smtp_server, self.smtp_port)
    #             server.starttls()
    #             server.login(self.email_sender, self.email_password)
    #             text = msg.as_string()
    #             server.sendmail(self.email_sender, absent_students_emails, text)
    #             server.quit()
    #             logging.info("Email notification sent to absent students.")
    #         except Exception as e:
    #             logging.error(f"Failed to send email notification. Error: {str(e)}")

    def send_email_notification(self, absent_students=None):
        if absent_students is None:
            # If absent_students is not provided, use the entire list of known students
            absent_students = self.face_name_known_list

        if absent_students:
            subject = "Attendance Notification"
            body = "Dear Parent,\n\nYour child was absent today."

            # Map names to email addresses
            absent_students_emails = [self.face_email_known_list[self.face_name_known_list.index(name)] for name in
                                      absent_students]

            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = ', '.join(absent_students_emails)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_sender, self.email_password)
                text = msg.as_string()
                server.sendmail(self.email_sender, absent_students_emails, text)
                server.quit()
                logging.info("Email notification sent to absent students.")
            except Exception as e:
                logging.error(f"Failed to send email notification. Error: {str(e)}")

    def send_sms_notification(self):
        for student in self.absent_students:
            # Twilio credentials
            account_sid = 'ACf3fd8e161ea88406b4c4e1784f3cc37e'
            auth_token = '0d79a82ec8ad04ae0f330bedeaa67889'
            twilio_phone_number = '+19285850330'

            # Initialize Twilio client
            client = Client(account_sid, auth_token)

            # Compose the message
            message = f"{student} is present today."

            try:
                # Send SMS notification
                client.messages.create(
                    body=message,
                    from_=twilio_phone_number,
                    to='+9779866442008'  # Replace with the recipient's phone number
                )
                logging.info(f"SMS notification sent to notify that {student} is present.")
            except Exception as e:
                logging.error(f"Failed to send SMS notification. Error: {str(e)}")

    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            path_features_known_csv = "data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)

            for i in range(csv_rd.shape[0]):
                features_someone_arr = []

                # Extract email (assumed to be at the beginning of each row)
                email = csv_rd.iloc[i][0].split('_')[1]  # Assuming email is in the format "name_email"
                name = csv_rd.iloc[i][0].split('_')[0]
                # Extract features
                for j in range(1, 129):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])

                self.face_name_known_list.append(name)
                self.face_email_known_list.append(email)
                self.face_features_known_list.append(features_someone_arr)

                # Print email for debugging purposes
                print(f"Student {i + 1} - Email: {email}")
                print(f"Student {i + 1} - Name: {name}")


            logging.info("Faces in Database: %d", len(self.face_features_known_list))
            return 1
        else:
            logging.warning("'features_all.csv' not found!")

            return 0

    def update_fps(self):
        now = time.time()
        # Refresh fps per second
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    @staticmethod
    def cosine_similarity(feature_1, feature_2):
        dot_product = np.dot(feature_1, feature_2)
        norm_feature_1 = np.linalg.norm(feature_1)
        norm_feature_2 = np.linalg.norm(feature_2)
        # print("Feature 1:", feature_1)
        # print("Feature 2:", feature_2)
        print("Dot Product:", dot_product)
        # print("Norm of Feature 1:", norm_feature_1)
        # print("Norm of Feature 2:", norm_feature_2)
        similarity = dot_product / (norm_feature_1 * norm_feature_2)
        print("Cosine Similarity:", similarity)  # Print the similarity value
        return similarity

    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            similarities_current_frame_person_x_list = []

            for j in range(len(self.last_frame_face_centroid_list)):
                similarity = self.cosine_similarity(
                    self.current_frame_face_feature_list[i],
                    self.face_features_known_list[j]
                )
                similarities_current_frame_person_x_list.append(similarity)

            last_frame_num = similarities_current_frame_person_x_list.index(
                max(similarities_current_frame_person_x_list))
            if similarities_current_frame_person_x_list[last_frame_num] > self.similarity_threshold:
                self.current_frame_face_name_list[i] = self.face_name_known_list[last_frame_num]

    def draw_note(self, img_rd):
        cv2.putText(img_rd, "Smart Attendance", (20, 40), self.font, 1, (255, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

        # for i in range(len(self.current_frame_face_name_list)):
        #     name = self.current_frame_face_name_list[i]
        #     similarity = self.current_frame_face_X_similarity_list[i]
        #     text = f"{name} (Similarity: {similarity:.2f})"
        #     img_rd = cv2.putText(img_rd, text,
        #                          self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
        #                          cv2.LINE_AA)

        for i in range(len(self.current_frame_face_name_list)):
            img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i],
                                 self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                 cv2.LINE_AA)
        return img_rd

    def attendance(self, name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, current_date))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"{name} is already marked as present for {current_date}")
        else:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            cursor.execute("INSERT INTO attendance (name, time, date) VALUES (?, ?, ?)",
                           (name, current_time, current_date))
            conn.commit()
            print(f"{name} marked as present for {current_date} at {current_time}")

            if name in self.absent_students:
                self.absent_students.remove(name)
                print(f"{name} removed from absent_students list")

            if name != 'unknown':
                self.absent_students.append(name)
                # self.send_sms_notification()

        conn.close()

    def process(self, stream):
        if self.get_face_database():
            while stream.isOpened():
                self.frame_cnt += 1
                logging.debug("Frame " + str(self.frame_cnt) + " starts")
                flag, img_rd = stream.read()
                kk = cv2.waitKey(1)

                faces = detector(img_rd, 0)

                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)

                self.last_frame_face_name_list = self.current_frame_face_name_list[:]
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

                if (self.current_frame_face_cnt == self.last_frame_face_cnt):
                    logging.debug("No face count changes in this frame")

                    self.current_frame_face_position_list = []

                    if "unknown" in self.current_frame_face_name_list:
                        self.reclassify_interval_cnt += 1

                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            img_rd = cv2.rectangle(img_rd,
                                                   tuple([d.left(), d.top()]),
                                                   tuple([d.right(), d.bottom()]),
                                                   (255, 255, 255), 2)

                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()

                    for i in range(self.current_frame_face_cnt):
                        img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i],
                                             self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                             cv2.LINE_AA)
                    self.draw_note(img_rd)

                else:
                    logging.debug("Faces count changes in this frame")
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_similarity_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    if self.current_frame_face_cnt == 0:
                        logging.debug("No faces in this frame")
                        self.current_frame_face_name_list = []

                    else:
                        logging.debug("Get faces in this frame and do face recognition")
                        self.current_frame_face_name_list = []
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                            self.current_frame_face_name_list.append("unknown")

                        for k in range(len(faces)):
                            logging.debug("For face %d in current frame:", k + 1)
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            self.current_frame_face_X_similarity_list = []

                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                            for i in range(len(self.face_features_known_list)):
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    similarity_tmp = self.cosine_similarity(
                                        self.current_frame_face_feature_list[k],
                                        self.face_features_known_list[i]
                                    )
                                    logging.debug("With person %d, the similarity: %f", i + 1, similarity_tmp)
                                    self.current_frame_face_X_similarity_list.append(similarity_tmp)
                                else:
                                    self.current_frame_face_X_similarity_list.append(0)

                            similar_person_num = self.current_frame_face_X_similarity_list.index(
                                max(self.current_frame_face_X_similarity_list))

                            if self.current_frame_face_X_similarity_list[similar_person_num] > self.similarity_threshold:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                                logging.debug("Face recognition result: %s",
                                              self.face_name_known_list[similar_person_num])

                                nam = self.face_name_known_list[similar_person_num]
                                print(type(self.face_name_known_list[similar_person_num]))
                                print(nam)
                                self.attendance(nam)
                            else:
                                logging.debug("Face recognition result: Unknown person")

                        self.draw_note(img_rd)

                if kk == ord('q'):
                    # absent_students = [name for name in self.face_name_known_list if name == 'unknown']
                    # if nam variable is null send notification as absent to all
                    # if nam variable has some data the send email except that name
                    print("Available name: ", self.face_name_known_list)

                    '''Previous code for sending notification'''
                    # absent_students = [name for name in self.face_name_known_list if name != nam]
                    # if absent_students:
                    #     self.send_email_notification(absent_students)
                    #     # self.send_email_notification()
                    #     print("Absent Student:", absent_students)
                    # break

                    # # Send email notification to absent students
                    # absent_students = [name for name in self.face_name_known_list if name in self.absent_students]
                    # if absent_students:
                    #     self.send_email_notification(absent_students)
                    #     print("Absent Students:", absent_students)
                    # break

                    # Determine absent students by subtracting recognized students from all known students
                    '''Prev notification'''
                    present_students = [name for name in self.face_name_known_list if name not in self.absent_students]
                    if present_students:
                        # Send email notification to absent students
                        self.send_email_notification(present_students)
                        print("Absent Students:", present_students)
                    break

                self.update_fps()
                cv2.namedWindow("camera", 1)
                cv2.imshow("camera", img_rd)

                logging.debug("Frame ends\n\n")

    def run(self):
        cap = cv2.VideoCapture(0)
        self.process(cap)
        # self.send_email_notification()
        cap.release()
        cv2.destroyAllWindows()


def main():
    logging.basicConfig(level=logging.INFO)
    Face_Recognizer_con = Face_Recognizer()
    Face_Recognizer_con.run()


if __name__ == '__main__':
    main()
