from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QLabel
from PySide6.QtGui import QPixmap, QImage, QScreen
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QImageCapture, QMediaDevices
from PySide6.QtMultimediaWidgets import QVideoWidget
import os
import csv
from datetime import datetime
import time
import sys

# 앱 경로 얻기 함수
def get_application_path():
    """애플리케이션의 실행 경로를 반환합니다."""
    if getattr(sys, 'frozen', False):
        # PyInstaller로 패키징된 경우
        application_path = os.path.dirname(sys.executable)
    else:
        # 일반 Python 스크립트로 실행된 경우
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path

# 사용자 문서 폴더 경로 얻기 함수
def get_user_documents_path():
    """사용자 문서 폴더 경로를 반환합니다."""
    try:
        import ctypes.wintypes
        CSIDL_PERSONAL = 5  # 내 문서
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, 0, buf)
        return buf.value
    except:
        # 실패 시 홈 디렉토리 사용
        return os.path.expanduser("~")

# UI 파일 로드 함수
def load_ui(ui_file):
    """UI 파일을 로드합니다."""
    from PySide6.QtUiTools import QUiLoader
    loader = QUiLoader()
    
    # 리소스 경로 확인
    app_path = get_application_path()
    ui_path = os.path.join(app_path, ui_file)
    
    print(f"UI 파일 경로: {ui_path}")
    
    if not os.path.exists(ui_path):
        print(f"UI 파일을 찾을 수 없습니다: {ui_path}")
        # 패키지 내부에서 찾기 시도
        if getattr(sys, 'frozen', False):
            ui_path = os.path.join(sys._MEIPASS, ui_file)
            print(f"대체 UI 경로 시도: {ui_path}")
    
    ui_file_obj = QtCore.QFile(ui_path)
    ui_file_obj.open(QtCore.QFile.ReadOnly)
    ui = loader.load(ui_file_obj)
    ui_file_obj.close()
    return ui

class MyForm(QtCore.QObject):
    def __init__(self):
        super().__init__()
        
        # 애플리케이션 경로 설정
        self.app_path = get_application_path()
        self.user_docs = get_user_documents_path()
        print(f"앱 경로: {self.app_path}")
        print(f"사용자 문서 경로: {self.user_docs}")
        
        # UI 로드
        self.window = load_ui("res/mainWin.ui")
        
        # 버튼 클릭 이벤트 연결
        self.window.btn_save.clicked.connect(self.save_clicked)
        self.window.btn_del.clicked.connect(self.delete_clicked)
        self.window.btn_camera.clicked.connect(self.camera_clicked)
        
        # 저장 디렉토리 생성 - 사용자 문서 폴더에 저장
        self.app_data_dir = os.path.join(self.user_docs, "카메라앱")
        self.save_dir = os.path.join(self.app_data_dir, "saved_data")
        self.photo_dir = os.path.join(self.app_data_dir, "saved_photos")
        
        # 필요한 디렉토리 생성
        for directory in [self.app_data_dir, self.save_dir, self.photo_dir]:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    print(f"디렉토리 생성됨: {directory}")
            except Exception as e:
                print(f"디렉토리 생성 오류: {directory} - {str(e)}")
            
        # 사진 관련 변수
        self.latest_photo = None
        
        # 카메라 설정
        self.setup_camera()
        
        # 시스템 메시지
        print("애플리케이션 초기화 완료")
    
    def setup_camera(self):
        try:
            # UI에서 카메라 화면을 표시할 라벨 가져오기
            self.camera_label = self.window.label_5
            
            # 카메라 인스턴스 생성 - 사용 가능한 첫 번째 카메라 사용
            available_cameras = QMediaDevices.videoInputs()
            if available_cameras:
                print(f"사용 가능한 카메라 {len(available_cameras)}대:", [c.description() for c in available_cameras])
                self.camera = QCamera(available_cameras[0])
            else:
                print("사용 가능한 카메라가 없습니다!")
                QMessageBox.warning(self.window, "경고", "사용 가능한 카메라가 없습니다.")
                self.camera = QCamera()
            
            # 미디어 캡처 세션 생성
            self.capture_session = QMediaCaptureSession()
            self.capture_session.setCamera(self.camera)
            
            # 비디오 출력 위젯 생성
            self.video_widget = QVideoWidget(self.window)
            self.video_widget.setGeometry(self.camera_label.geometry())
            self.capture_session.setVideoOutput(self.video_widget)
            
            # 카메라 시작
            self.camera.start()
            
            print("카메라 설정 완료 - 2초 대기 중...")
            # 카메라 초기화를 위한 대기 시간
            QApplication.processEvents()
            time.sleep(2)  # 카메라가 시작될 시간을 주기 위해 2초 대기
            print("카메라 초기화 완료")
            
        except Exception as e:
            print(f"카메라 설정 중 오류 발생: {str(e)}")
            QMessageBox.critical(self.window, "오류", f"카메라 설정 중 오류가 발생했습니다: {str(e)}")
    
    def save_clicked(self):
        name = self.window.lineEdit_name.text()
        phone = self.window.lineEdit_PHnum.text()
        
        # 입력 검증
        if not name or not phone:
            QMessageBox.warning(self.window, "경고", "이름과 전화번호는 필수 입력 항목입니다.")
            return
            
        # CSV 파일에 저장
        filename = os.path.join(self.save_dir, "contacts.csv")
        file_exists = os.path.exists(filename)
        
        try:
            print(f"CSV 파일 저장 시도: {filename}")
            # 한국어 Windows 환경에서 잘 호환되는 cp949(euc-kr) 인코딩 사용
            with open(filename, 'a', newline='', encoding='cp949') as f:
                writer = csv.writer(f)
                
                # 파일이 존재하지 않으면 헤더 작성
                if not file_exists:
                    writer.writerow(["이름", "전화번호", "사진 파일"])
                
                # 사진 파일 경로 추가
                photo_path = self.latest_photo if self.latest_photo else ""
                
                # 데이터 작성
                writer.writerow([name, phone, photo_path])
            
            QMessageBox.information(self.window, "알림", f"데이터가 {filename}에 CSV 형식으로 저장되었습니다.")
            print(f"CSV 저장 완료: 이름={name}, 전화번호={phone}, 사진={photo_path}")
        except Exception as e:
            QMessageBox.critical(self.window, "오류", f"저장 중 오류 발생: {str(e)}")
            print(f"저장 오류: {str(e)}")
            import traceback
            traceback.print_exc()
        
    def delete_clicked(self):
        self.window.lineEdit_name.clear()
        self.window.lineEdit_PHnum.clear()
        self.latest_photo = None
        print("초기화 버튼 클릭: 모든 필드가 초기화되었습니다.")
        
    def camera_clicked(self):
        try:
            # 카메라 위젯이 보이는지 확인
            if not self.video_widget.isVisible():
                QMessageBox.warning(self.window, "경고", "카메라 화면이 표시되지 않습니다. 카메라를 확인해주세요.")
                return
            
            print("스크린샷 촬영 시도...")
            
            # 화면 캡처 방식으로 변경
            widget_rect = self.video_widget.rect()
            global_pos = self.video_widget.mapToGlobal(widget_rect.topLeft())
            screenshot = QApplication.primaryScreen().grabWindow(
                0,  # 0은 전체 화면을 의미
                global_pos.x(),
                global_pos.y(),
                widget_rect.width(),
                widget_rect.height()
            )
            
            if screenshot.isNull():
                print("스크린샷이 NULL입니다.")
                QMessageBox.warning(self.window, "경고", "카메라 화면을 캡처할 수 없습니다.")
                return
                
            # 현재 시간으로 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            photo_filename = os.path.join(self.photo_dir, f"photo_{timestamp}.jpg")
            
            # 스크린샷 저장
            print(f"이미지 저장 시도: {photo_filename}")
            saved = screenshot.save(photo_filename)
            
            if saved:
                self.latest_photo = photo_filename
                # 캡처한 이미지를 라벨에도 표시
                scaled_pixmap = screenshot.scaled(
                    self.camera_label.width(), 
                    self.camera_label.height(), 
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio
                )
                self.camera_label.setPixmap(scaled_pixmap)
                
                QMessageBox.information(self.window, "알림", f"사진이 {photo_filename}에 저장되었습니다.")
                print(f"사진 저장 완료: {photo_filename}")
            else:
                QMessageBox.critical(self.window, "오류", f"사진을 {photo_filename}에 저장할 수 없습니다.")
                print(f"사진 저장 실패: {photo_filename}")
            
        except Exception as e:
            QMessageBox.critical(self.window, "오류", f"사진 촬영 중 오류 발생: {str(e)}")
            print(f"사진 촬영 오류: {str(e)}")
            import traceback
            traceback.print_exc()

app = QApplication([])
form = MyForm()
form.window.show()
app.exec()