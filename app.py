from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from partida import JogoDaVelha

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = []
partidas = []

@app.route("/")
def home():
    jogador = request.args.get('username')
    sala = request.args.get('sala_id')
    
    if jogador is not None and sala is not None:
        print('jogador: ', jogador)
        print('sala: ', sala)
        for partida in partidas:
            if partida.partidaID == sala:
                if partida.jogador1 == '':
                    partida.jogador1 = jogador
                    print('partida.jogador1: ', partida.jogador1)
                    return render_template('jogo.html', username=jogador, sala_id=sala, jogador1=partida.jogador1, jogador2=partida.jogador2, peca1=partida.Pecajogador1, peca2=partida.Pecajogador2, jogador_atual=partida.vez)
                elif partida.jogador2 == '':
                    partida.jogador2 = jogador
                    print('partida.jogador2: ', partida.jogador2)
                    return render_template('jogo.html', username=jogador, sala_id=sala, jogador1=partida.jogador1, jogador2=partida.jogador2, peca1=partida.Pecajogador1, peca2=partida.Pecajogador2, jogador_atual=partida.vez)
                else:
                    return render_template('index.html', error='jogo_cheio')
        jogo = JogoDaVelha(partidaID=sala, jogador1=jogador, jogador2='')
        partidas.append(jogo)
        
        return render_template('jogo.html', username=jogador, sala_id=sala, jogador1=jogo.jogador1, jogador2=jogo.jogador2, peca1=jogo.Pecajogador1, peca2=jogo.Pecajogador2, jogador_atual=jogo.vez)
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html")

@app.route("/partida")
def partida():
    _partida = JogoDaVelha()
    return render_template("jogo.html")
    
@socketio.on('sendMessage', namespace='/partida')
def send_message_handler(msg):
    messages.append(msg)
    emit('getMessage', msg, broadcast=True, to=msg["sala_id"])

@socketio.on('message', namespace='/partida')
def message_handler(msg):
    send(messages)

@socketio.on('sendJogada', namespace='/partida')
def send_jogada_handler(obj):
    obj['vez'] = 'x' if obj['vez'] == 'o' else 'o'
    for partida in partidas:
        if partida.partidaID == obj['sala_id']:
            jogo = partida
            print('jogo: ', jogo)
            break
    jogo.qtdjogada = jogo.qtdjogada + 1
    if obj['casa'] == 1:
        jogo.casa1 = obj['jogada']
    elif obj['casa'] == 2:
        jogo.casa2 = obj['jogada']
    elif obj['casa'] == 3:
        jogo.casa3 = obj['jogada']
    elif obj['casa'] == 4:
        jogo.casa4 = obj['jogada']
    elif obj['casa'] == 5:
        jogo.casa5 = obj['jogada']
    elif obj['casa'] == 6:
        jogo.casa6 = obj['jogada']
    elif obj['casa'] == 7:
        jogo.casa7 = obj['jogada']
    elif obj['casa'] == 8:
        jogo.casa8 = obj['jogada']
    elif obj['casa'] == 9:
        jogo.casa9 = obj['jogada']
    resultado = jogo.verificarTabuleiro()
    if resultado == "continua":
        obj["resultado"] = 1
    elif resultado == "empate":
        obj["resultado"] = 0
        jogo.resetaTabuleiro()
    elif resultado == "x":
        jogo.pontosjogador1 = jogo.pontosjogador1 + 1
        jogo.resetaTabuleiro()
        obj["resultado"] = "x"
    elif resultado == "o":
        jogo.pontosjogador2 = jogo.pontosjogador2 + 1
        jogo.resetaTabuleiro()
        obj["resultado"] = "o"
    emit('getJogada', obj, broadcast=True, to=obj['sala_id'])

@socketio.on('attjogador1', namespace='/partida')
def attjogador1_handler(obj):
    emit('getjogador2', obj, broadcast=True, to=obj['sala_id'])

@socketio.on('join', namespace='/partida')
def join_handler(sala):
    join_room(sala['sala_id'])
    print('join: ', sala)
    emit('joined', {'msg': sala["username"]+' joined'}, to=sala['sala_id'])

@socketio.on('placar', namespace='/partida')
def placar_handler(obj):
    emit('alteraPlacar', obj, to=obj['sala_id'])

@socketio.on('connect', namespace='/partida')
def connect_handler(auth):
    print('partidas: ', partidas)

if __name__ == '__main__':
    socketio.run(app, debug=True)