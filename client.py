import socket
import json

name = input('>> name: ')

HOST = '127.0.0.1'
PORT = 8080

# address family : IPv4 , Socket type : TCP(Stream)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print ('>> Connect Server')

while True:
    print(">> [exit: 0, normal: 1, upper: 2, lower: 3]")
    echo_type = input('>> echo type: ')
    if echo_type == '0':
        break
    elif not (echo_type == '1' or echo_type == '2' or echo_type == '3') :
        continue

    message = input('>> ')

    # header
    ### header type = 1byte(echo type 지정)
    ### body length = 2byte
    header = [int(echo_type)]

    # body
    ### json 
    ### name, message 
    body_dict = {}
    body_dict["name"] = name
    body_dict["message"] = message
    body = json.dumps(body_dict)

    # header와 body로 송신 데이터 생성(bytes형)
    send_data = bytearray(header)
    body_len = len(body)
    ### .to_bytes는 python 3.1 이상에서 사용 가능 / 현재 빅엔디안 방식을 사용
    send_data += bytearray(body_len.to_bytes(2, byteorder="big"))
    send_data += bytes(body,'utf-8')

    # 데이터 전송
    client_socket.sendall(send_data)

    # 서버로부터 데이터 수신
    recv_data = client_socket.recv(1024)

    ### header 추출
    # header = recv_data[:3]
    # echo_type = header[0]
    # body_len = 256 * header[1] + header[2]

    # header 미사용으로 body만 추출
    body = recv_data[3:]

    # json 파일을 딕셔너리 형식으로 변환
    body_dict = eval(body.decode("utf-8"))

    # 메세지만 출력
    print(">>",body_dict["message"])


client_socket.close()