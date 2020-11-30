from flask import abort ,Flask, flash,g , redirect ,render_template, request, session, url_for
from werkzeug.utils import secure_filename
import os

class User:
    def __init__(self, id, username,password):
        self.id=id
        self.username=username
        self.password=password

    def __repr__(self):
        return f'{self.username} ({self.id}) ' 
class Emb:
    def __init__(self,cod,net,bru,tip):
        self.cod=cod
        self.net=net
        self.bru=bru
        self.tip=tip
class Var:
    def __init__(self,cod,nom):
        self.cod=cod
        self.nombre=nom
class Esp:
    def __init__(self,cod,nom):
        self.cod=cod
        self.nombre=nom
class Guia:
    def __init__(self,num,cont,especie,variedad,cajas,pallets,neto,bruto,emb,chn,cht,nave,puerto,destino):
        self.numero=num
        self.contenedor = cont
        self.especie = especie
        self.variedad = variedad
        self.cajas = cajas
        self.neto = neto
        self.bruto = bruto
        self.embalaje = emb
        self.nombre_chofer = chn
        self.tel_chofer = cht
        self.nave=nave
        self.puerto=puerto
        self.destino=destino
        self.pallets=pallets
        self.emb_neto = None
        self.emb_bruto = None
        self.pallets_a = []
        

users = []
users.append(User(0,"rorritog","asdf"))
users.append(User(1,"rpa","fj2349jfsjdkj234lkj6sdflsdn43"))

embalajes = []
embalajes.append(Emb("CAR82",7.2,8.2,"Cartón"))
embalajes.append(Emb("CAR72",6.2,7.2,"Cartón"))
embalajes.append(Emb("CAR100",9.0,10.0,"Cartón"))
embalajes.append(Emb("CAR90",8.0,9.0,"Cartón"))
embalajes.append(Emb("PLA82",7.2,8.2,"Plástico"))
embalajes.append(Emb("PLA72",6.2,7.2,"Plástico"))
embalajes.append(Emb("PLA100",9.0,10.0,"Plástico"))
embalajes.append(Emb("PLA90",8.0,9.0,"Plástico"))
embalajes.append(Emb("BIN82",7.2,8.2,"Bin Madera"))
embalajes.append(Emb("BIN72",6.2,7.2,"Bin Madera"))
embalajes.append(Emb("BIN100",9.0,10.0,"Bin Madera"))
embalajes.append(Emb("BIN90",8.0,9.0,"Bin Madera"))
embalajes.append(Emb("PBD82",7.2,8.2,"Plástico Biodegradable"))
embalajes.append(Emb("PBD72",6.2,7.2,"Plástico Biodegradable"))
embalajes.append(Emb("PBD100",9.0,10.0,"Plástico Biodegradable"))
embalajes.append(Emb("PBD90",8.0,9.0,"Plástico Biodegradable"))

variedades = []
variedades.append(Var(1,"Fresh"))
variedades.append(Var(2,"Frozen"))
#variedades.append(Var(3,"Seedless"))
variedades.append(Var(4,"Special"))
variedades.append(Var(5,"Premium"))
variedades.append(Var(6,"Usda"))

especies = []
especies.append(Esp("UV","Uvas"))
especies.append(Esp("NAR","Naranjas"))
especies.append(Esp("NEC","Nectarines"))
#especies.append(Esp("GUI","Guindas"))
especies.append(Esp("CER","Cerezas"))
especies.append(Esp("MAN","Mandarinas"))
especies.append(Esp("DUR","Duraznos"))
especies.append(Esp("PLA","Plátanos"))
especies.append(Esp("PAL","Paltas"))
especies.append(Esp("NUE","Nueces"))

puertos = {
    'VAL': 'Valparaíso',
    'SAT': 'San Antonio',
    'LGP': 'London Gateway Port',
    'LIV': 'Liverpool',
    'SNG': 'Shangai',
    'HKG': 'Hong Kong',
    'PHI': 'Philadelphia',
    'KAP': 'King Abdula Port'
}

guias = []

contenedores = ["test"]
contenedores_embarcados = {
    'a': ["asd","asds"]

}

uploaded_file_filename = None
app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploaded/'
@app.before_request
def before_request():
    g.user = None
    g.nave = None
    if 'user_id' in session:
        user =[x for x in users if x.id==session['user_id']][0]
        g.user = user

    g.embalajes = embalajes
    g.variedades = variedades
    g.especies = especies
# Creating simple Routes 
@app.route('/login', methods=['GET','POST'])
def login():
    session.pop('user_id',None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user =[x for x in users if x.username==username]
        if user:
            if password == user[0].password:
                session['user_id'] = user[0].id
                return redirect(url_for('home'))
            else:
                flash('Password incorrecto')
                return redirect(url_for('login'))
        else:
            flash('Usuario no existe')
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/forbbiden')
def forb():
    return abort(403)

# Routes to Render Something
@app.route('/')
def home():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("home.html")

@app.route('/tablas/embalajes',methods=['GET','POST'])
def tablas_emb():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        embalajes.append(Emb(request.form['ce_codigo'],request.form['ce_pneto'],request.form['ce_pbruto'],request.form['ce_tipo']))
    
    return render_template("tablas_emb.html")

@app.route('/tablas/variedades',methods=['GET','POST'])
def tablas_var():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        variedades.append(Var(int(request.form['var_code']),request.form['var_name']))
    
    return render_template("tablas_var.html")
    
@app.route('/tablas/especies',methods=['GET','POST'])
def tablas_esp():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        especies.append(Var(request.form['esp_code'],request.form['esp_name']))
    
    return render_template("tablas_esp.html")

@app.route('/despachos/resumenguia/',methods=['GET','POST'])
def resumen_guia():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        for i in guias:
            if i.numero == request.form['numero_guia']:
                i.bruto=round(i.bruto,1)
                i.neto=round(i.neto,1)
                g.guia = i
                break
        
    if request.method == 'GET':
        g.guia = None
            
    return render_template('resumen_guia.html')

@app.route('/despachos/embarcarcontenedor/',methods=['GET','POST'])
def emb_contenedor():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form['numero_cont'] in contenedores:
            for i in contenedores_embarcados.values():
                if request.form['numero_cont'] in i:
                   g.embarcarcontenedor_code=3 
                   return render_template('embarcar_contenedor.html')

            if request.form['nombre_nave'] in contenedores_embarcados.keys():
                contenedores_embarcados[request.form['nombre_nave']].append(request.form['numero_cont'])
                g.embarcarcontenedor_code=1
            else:
                contenedores_embarcados[request.form['nombre_nave']]=[request.form['numero_cont']]
                g.embarcarcontenedor_code=2

        else:
            #contenedor no existe
            g.embarcarcontenedor_code = 0
        
    if request.method == 'GET':
        g.embarcarcontenedor_code = None
            
    return render_template('embarcar_contenedor.html')


@app.route('/documentos/resumenembarque/',methods=['GET','POST'])
def resumen_embarque():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        g.show_resumen = True
        if request.form['nombre_nave'] in contenedores_embarcados.keys():
            g.nave= contenedores_embarcados[request.form['nombre_nave']]
            g.nave_nombre = request.form['nombre_nave'] 
        else:
             g.nave = None
        
    if request.method == 'GET':
        g.show_resumen = False
        g.nave = None
            
    return render_template('resumen_embarque.html')

@app.route('/avisos/finalizacionembarque/',methods=['GET','POST'])
def finalizacion_embarque():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        #estamos consultado por nava
        if 'nombre_nave' in request.form.keys():
            if request.form['nombre_nave'] in contenedores_embarcados.keys():
                g.fin_nave_nombre = request.form['nombre_nave'] 
            else:
                g.fin_nave_nombre = 'null'
        #queremos comfirmarlo
  
         
    if request.method == 'GET': 
        g.fin_nave_nombre = None
        return render_template('finalizacion embarque.html') 
            
    return render_template('finalizacion embarque.html')

@app.route('/embarques/ingresotxt',methods=['GET','POST'])
def txt_upload():   
    global uploaded_file_filename
    if request.method == 'POST':
        if 'filename' in request.files.keys():

            file = request.files['filename']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            g.upload_errors = 1
            file_content = []
            
            uploaded_file_filename=filename
            for line in open(app.config['UPLOAD_FOLDER']+filename,"r"):
                
                translated_line = ""
                stripped_line = line.strip("\n")
                for index,code in enumerate(stripped_line.split(",")):
                    if index == 1:
                        translated_line+=puertos[code]+","
                    elif index == 2:
                        translated_line+=puertos[code]+","
                    elif index == 7:
                        found = False
                        for i in especies:
                            if code == i.cod:
                                translated_line+=i.nombre+","
                                found = True
                        if not found:
                            translated_line+="NOT FOUND,"
                            g.upload_errors = 2
                    elif index == 8:
                        found = False
                        for i in variedades:
                            if int(code) == i.cod:
                                translated_line+=i.nombre+","
                                found = True
                        if not found:
                            translated_line+="NOT FOUND,"
                            g.upload_errors = 2
                    
                    elif index == 9:
                        found = False
                        for i in embalajes:
                            if code == i.cod:
                                translated_line+=i.cod+","
                                found = True
                        if not found:
                            translated_line+="NOT FOUND,"
                            g.upload_errors = 2
                    #ultima linea
                    elif index == 11:
                        translated_line+=code
                    else:
                        translated_line+=code+","
            
                file_content.append(translated_line)
                
            g.file_content = file_content
        else:
            for line in open(app.config['UPLOAD_FOLDER']+uploaded_file_filename,"r"):
                data = line.split(",")
                found = False
                for i in guias:
                    if i.numero == data[3]:
                        found=True
                        i.cajas+=int(data[6])
                        i.bruto+=round(i.emb_bruto*int(data[6]),1)
                        i.neto+=round(i.emb_neto*int(data[6]),1)

                        if data[5] not in i.pallets_a:
                            i.pallets_a.append(data[5])
                            i.pallets+=1
                        break

                if not found:
                    #crear guia
                    cod_var= None
                    for var in variedades:
                        if var.cod == int(data[8]):
                            cod_var=var.nombre
                            break
                    cod_esp= None
                    for var in especies:
                        if var.cod == data[7]:
                            cod_esp=var.nombre
                            break
                    neto=0
                    bruto=0
                    for emb in embalajes:
                        if emb.cod == data[9]:
                            neto=float(emb.net)
                            bruto=float(emb.bru)
                            break
                    cajas = int(data[6])
                    #round(,1)
                    guia = Guia(data[3],data[4],cod_esp,cod_var,cajas,1,round(cajas*neto,1),round(cajas*bruto,1),data[9],data[10],data[11],data[0],puertos[data[1]],puertos[data[2]])
                    guia.pallets_a.append(data[5])
                    guia.emb_neto=neto
                    guia.emb_bruto=bruto
                    guias.append(guia)
                    contenedores.append(data[4])

            g.upload_errors = 3
            #botón de confirmación
            return render_template('upload_txt.html')

    if request.method == 'GET': 
        g.upload_errors = 0
        uploaded_file_filename = None

        return render_template('upload_txt.html')
            
     
            
    return render_template('upload_txt.html')































if __name__ == '__main__':
    app.run(debug=True)
