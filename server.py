import socket
import json


def start_connection(client_socket, addr):
    print('>> Connected by ' + addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때까지 반복
    while True:
        try:
            # 클라이언트로부터 데이터 수신
            recv_data = client_socket.recv(1024)
            if not recv_data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0], ':', addr[1])

            # header 추출       
            header = recv_data[:3]
            echo_type = header[0]
            body_len = 256 * header[1] + header[2]

            # body 추출
            body = recv_data[3:]
            body_dict = eval(body.decode("utf-8"))

            # 메세지 처리 전 출력
            print('>> Befor : [' + body_dict["name"] + '] :', body_dict["message"])

            # 메세지 처리
            if echo_type == 2:
                body_dict["message"] = body_dict["message"].upper()
            elif echo_type == 3:
                body_dict["message"] = body_dict["message"].lower()

                # 메세지 처리 후 출력
            print('>> After : [' + body_dict["name"] + '] :', body_dict["message"])

            # header 재생성
            header = [int(echo_type)]

            # json형식 body 생성
            body = json.dumps(body_dict)

            # header와 body로 송신 데이터 생성(bytes형)
            send_data = bytearray(header)
            body_len = len(body)
            ### .to_bytes는 python 3.1 이상에서 사용 가능 / 현재 빅엔디안 방식을 사용
            send_data += bytearray(body_len.to_bytes(2, byteorder="big"))
            send_data += bytes(body, 'utf-8')

            # 데이터가 수신되면 클라이언트에 다시 전송(에코)
            client_socket.sendall(send_data)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


# 서버 IP 및 열어줄 포트
HOST = '127.0.0.1'
PORT = 8080

# 서버 소켓 생성
### address family : IPv4 , Socket type : TCP(Stream)
print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

try:
    # 클라이언트 접속 대기 및 연결
    while True:
        print('>> Wait')
        client_socket, addr = server_socket.accept()
        start_connection(client_socket, addr)

except Exception as e:
    print('error:', e)

finally:
    server_socket.close()
