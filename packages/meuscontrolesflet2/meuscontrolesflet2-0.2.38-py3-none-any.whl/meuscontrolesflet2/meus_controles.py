
# from flet import(
# ft.UserControl,Control,Alignment,ft.FilePickerResultEvent,Page,app,
# Row,TextField, Text, Slider,BorderSide, colors,Border, border,
# BoxShadow,Offset,ShadowBlurStyle,LinearGradient,GradientTileMode,
# Container,TextButton,Column,Tab,Tabs,AlertDialog,ft.MainAxisAlignment,
# ft.DataTable, TextThemeStyle,IconButton, icons, DataColumn,
# DataCell,TextAlign,FontWeight, Dropdown, dropdown, TextStyle,
# DataRow, ElevatedButton
# )
# from flet import*
import subprocess
import inspect
import flet as ft
from threading import Thread
from time import time, sleep
from pandas import DataFrame, to_datetime
from datetime import datetime
import datetime
from re import findall
from pyperclip import copy
import json,pyautogui
import pickle
from pyautogui import position, click
import keyboard as kb
from flet_core.text import*
from flet_core.textfield import*
from  tkinter import Tk
import os
import PyInstaller.__main__
from shutil  import rmtree


def SalvarDadosLocais(self, nome, valor):
    self.page.client_storage.set(nome, valor)
    

def LerDadosLocais(self, nome,  default=None):
    if self.page.client_storage.contains_key(nome):
        return self.page.client_storage.get(nome)
    else:
        return default

def AbrirPDF(arquivo_pdf):
    caminho_chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    subprocess.Popen([caminho_chrome, arquivo_pdf])

def OrdenarDicionario(dic, col):
    coluna_old = dic[col]
    ord = sorted(dic[col])
    novo_index = [coluna_old.index(i) for i in ord]
    for i in dic.keys():
        dic[i]= [dic[i][k] for k in novo_index ]
    return dic

def ConverterListadeListaParadiciomarioColunas(listadelistas, chaves):
    dic = {i:[] for i in chaves}
    for i in range(len(chaves)):
        l = []
        for j in range(len(listadelistas)):
            l.append(listadelistas[j][i])
        dic[chaves[i]].extend(l)
    return dic

def ConverterListadeListaParaDicionario(listaDeLista):
    if isinstance(listaDeLista, list) and isinstance(listaDeLista[0], list):
        return {i[0]:i[1:]for i in listaDeLista}
    else:
        raise('lista de lista inválida')

def MatarProcesso(process_name = "main.exe"):
    comando = f"taskkill /F /IM {process_name}"
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    if resultado.returncode == 0:
        print(f"Processo {process_name} finalizado com sucesso.")
    else:
        print(f"Erro ao finalizar o processo {process_name}: {resultado.stderr}")

def get_screen_dimensions():
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

def listar_ambientes_virtuais(pasta):
    ambientes = []
    for nome in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, nome)
        if os.path.isdir(caminho_completo):
            # Verifica se o diretório tem a estrutura de um ambiente virtual
            if (os.path.exists(os.path.join(caminho_completo, 'bin', 'activate')) or
                os.path.exists(os.path.join(caminho_completo, 'Scripts', 'activate.bat'))):
                ambientes.append(nome)
    return ambientes


def escrever_json(self, data, filename):
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def ler_json(self, filename, default=None):
    if not filename.endswith('.json'):
        filename += '.json'
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        try:
            self.escrever_json(default, filename)
        except:
            pass
        return default or {}


def SalvarPickle( var, nome):
    with open(nome+'.plk', 'wb') as arquivo:
        pickle.dump(var, arquivo)

def LerPickle(nome):
    if not nome.endswith('.plk'):
        nome += '.plk'
    if os.path.isfile(nome):
        with open(nome, 'rb') as arquivo:
            return pickle.load(arquivo)
    else:
        return None  


def VerificarTemaNativo():
    if self.page.platform_brightness.name == 'Dark':
        print('tema escuro')
    elif self.page.platform_brightness.name == 'LIGHT':
        print('tema claro')

def VerificarWeb():
    if self.page.web:
        print('App Web')
    else:
        print('tema destop')

            
class TemaSelectSysten(ft.IconButton):
    def __init__(self):
        super().__init__()    
        self.pastalocal = 'TEmas_flet'
        self.verificar_pasta()
       
        self.EditarTema = self.JanelaEditarTema()
        self.icon = ft.icons.PALETTE
        self.sair = ft.FilledTonalButton('Sair', on_click=self.RestaurarJanela)
        self.em_edicao = False

        self.on_click = self.Edit


    def did_mount(self):
        self.ct_old = self.page.controls.copy() 
        try:       
            with open('mytheme.txt', 'r') as arq:
                tema = arq.read()
        except:
            tema = None
        if tema:
            self.page.bgcolor = 'surface'
            self.dic_atributos = self.arquiv[tema].copy()

        #     cores_claras = ["white","deeppurple","indigo","lightblue","lightgreen","lime"
        # "yellow","bluegrey","grey"]
        #     cc = []
        #     for i in cores_claras:
        #         cc.extend([f"{i}{j}" for j in range(100, 600,100)])
        #     cores_claras += cc

            if self.dic_atributos.get("light", False):
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.DARK


            self.page.theme = ft.Theme(
                color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
                color_scheme=ft.ColorScheme(
                    primary = self.dic_atributos["primary"],
                    on_primary = self.dic_atributos["on_primary"],
                    on_secondary_container = self.dic_atributos["on_secondary_container"],
                    outline = self.dic_atributos["outline"],
                    shadow = self.dic_atributos["shadow"],
                    on_surface_variant = self.dic_atributos["on_surface_variant"],
                    surface_variant = self.dic_atributos["surface_variant"],
                    primary_container = self.dic_atributos["primary_container"],
                    on_surface = self.dic_atributos["on_surface"],
                    surface = self.dic_atributos["surface"],
                    # on_primary_container = self.dic_atributos["on_primary_container"],
                    # secondary = self.dic_atributos["secondary"],
                    # on_secondary = self.dic_atributos["on_secondary"],
                    # tertiary = self.dic_atributos["tertiary"],
                    # on_tertiary = self.dic_atributos["on_tertiary"],
                    # tertiary_container = self.dic_atributos["tertiary_container"],
                    # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                    # error = self.dic_atributos["error"],
                    # on_error = self.dic_atributos["on_error"],
                    # error_container = self.dic_atributos["error_container"],
                    # on_error_container = self.dic_atributos["on_error_container"],
                    # background = self.dic_atributos["background"],
                    # on_background = self.dic_atributos["on_background"],
                    # outline_variant = self.dic_atributos["outline_variant"],
                    # scrim = self.dic_atributos["scrim"],
                    # inverse_surface = self.dic_atributos["inverse_surface"],
                    # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                    # inverse_primary = self.dic_atributos["inverse_primary"],
                    # surface_tint = self.dic_atributos["surface_tint"],
                )
            )
                
            for i in list(self.dic_atributos.keys()):
            #     self.icones[i].color = self.dic_atributos[i]
                try:
                    self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
                except:
                    pass
            self.menus.update()                  
            self.page.update()
        


    def verificar_pasta(self):
        user_profile = os.environ.get('USERPROFILE')
        # print(user_profile)
        if not user_profile:
            # return False  # USERPROFILE não está definido
            self.local = None

        caminho = os.path.join(user_profile, self.pastalocal)
        
        if os.path.exists(caminho):
            self.local = caminho
            # return self.caminho
        else:
            os.mkdir(caminho)
            # print(caminho)
            if os.path.exists(caminho):
                self.local = caminho
                # return self.caminho
            # else:
                # return None
    
    def caminho(self, nome):
        # self.verificar_pasta()
        return os.path.join(self.local, nome)


    def Edit(self, e):
        if not self.em_edicao:
            self.em_edicao = True
            self.tamanho_old = self.page.window.width,self.page.window.height
            self.page.window.width = 550
            self.page.window.height = 750
            self.page.controls = [ft.ListView([self.EditarTema,self.sair], expand=True)]
            self.page.update()

    def RestaurarJanela(self, e):
        e.page.window.width,e.page.window.height = self.tamanho_old
        e.page.controls = self.ct_old
        e.page.update()
        self.em_edicao = False


    def GerarMenus(self, i):
        return ft.PopupMenuButton(
            content = ft.Container(
                ft.Text(self.funcoes[i], no_wrap=False,), 
                border=ft.border.all(5,'blue'),
                padding = ft.Padding(5,0,5,0),
                margin=0,
                border_radius=12,
                

            ),                        
            splash_radius = 0,
            tooltip = '',
            items=[
                ft.PopupMenuItem(
                    content = self.paleta(i), 
                                            
                ),
                ft.PopupMenuItem(
                    content = self.GerarCores(i),                          
                ),                            
                
            ],
            col = 1 if len(self.funcoes[i]) <= len('labels, cor da caixa do checkbox e cor do check do popMenubutton') else 3
        
        
        ) 



    def Change_dark_light(self, e):
        match e.data:
            case "DARK":
                e.page.theme_mode = ft.ThemeMode.DARK
                self.dic_atributos["light"] = False
            case "LIGHT":
                e.page.theme_mode = ft.ThemeMode.LIGHT
                self.dic_atributos["light"] = True
        e.page.update()

    def JanelaEditarTema(self):
        self.cores = [
            "white","black","red","pink","purple",
            "deeppurple","indigo", "blue","lightblue",
            "cyan","teal","green","lightgreen","lime"
        "yellow", "amber", "orange", "deeporange",
        "brown","bluegrey","grey"

        ]
        self.funcoes = {
            'primary': 'primary: texto principal, fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone,  texto do elevatebuton',
            'on_primary': 'on_primary: texto filledbutton e bolinha do swicth com True',
            'on_secondary_container': 'on_secondary_container: texto filledtonalbutton',
            'outline': 'outline: borda do outliedbutton',
            'shadow': 'shadow: sombras',
            'on_surface_variant': 'on_surface_variant: labels, cor da caixa do checkbox e cor do check do popMenubutton',
            'surface_variant': 'surface_variant: slider e fundo do texfield e do dropbox',
            'primary_container': 'primary_container: HOVERED da bolinha do switch',
            'on_surface': 'on_surface: HOVERED do checkbox e cor dos items do popmenubuton',
            'surface': 'surface: cor de fundo',
            'color_scheme_seed':'color_scheme_seed',

        }
        self.atributos_ColorScheme = list(self.funcoes.keys())
        
        self.dic_atributos = {i:None for i in self.atributos_ColorScheme}
        self.icones = {i:ft.Icon(name = ft.icons.SQUARE, data = [i, False], color = 'white') for i in self.atributos_ColorScheme}
        
        self.nome_tema = ft.TextField(hint_text='Digite o nome do tema', col = 24)
        self.conf = False
        self.confirmar = ft.FilledButton('Confirmar', on_click= self.Salvar)
        self.cancelar = ft.FilledButton('Cancelar', on_click= self.Cancelar)
        self.linha_salve = ft.ResponsiveRow([self.nome_tema, self.confirmar, self.cancelar], columns=48,visible = False, col =96)
        self.btn_save = ft.FilledButton('Salvar Tema', on_click=self.TornarVizivel, col = 24)
        # self.color_scheme_seed = self.GerarMenus('color_scheme_seed', 50)
               
        self.select_dark_light = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value='DARK', label="DARK",label_style= ft.TextStyle(weight='BOLD')),
                    ft.Radio(value="LIGHT", label="LIGHT",label_style= ft.TextStyle(weight='BOLD')),
                
                ]
            ),
        on_change=self.Change_dark_light,
        )

        
  
        self.arquivo_temas = self.caminho('Tema')
        self.arquiv = self.ler_json(self.arquivo_temas, 
        default=  {
                "black": {
                    "background": None,
                    "error": None,
                    "error_container": None,
                    "inverse_primary": None,
                    "inverse_surface": None,
                    "on_background": None,
                    "on_error": None,
                    "on_error_container": None,
                    "on_inverse_surface": None,
                    "on_primary": "limeyellow",
                    "on_primary_container": None,
                    "on_secondary": None,
                    "on_secondary_container": "grey",
                    "on_surface": "cyan",
                    "on_surface_variant": "lightgreen",
                    "on_tertiary": None,
                    "on_tertiary_container": None,
                    "outline": "bluegrey",
                    "outline_variant": None,
                    "primary": "lightblue",
                    "primary_container": "grey",
                    "scrim": None,
                    "secondary": None,
                    "secondary_container": "white",
                    "shadow": "bluegrey",
                    "surface": "limeyellow",
                    "surface_tint": None,
                    "surface_variant": "limeyellow",
                    "tertiary": None,
                    "tertiary_container": None
    }
}                       
        )
        self.tema_escolhido = ft.Dropdown(
            label='Selecione um tema',
            col = 3,
            options = [
                ft.dropdown.Option(i)
                for i in sorted(list(self.arquiv.keys()))
            ],
            on_change=self.CarregarTema
        )

        self.menus = {i:self.GerarMenus(i) for i in self.atributos_ColorScheme}
        self.ferramentas = ft.Container(
            bgcolor=ft.colors.SURFACE,           
            expand=True,
            content = ft.ResponsiveRow(
                [

                    ft.ElevatedButton('Botão',
                        # color = self.cor3            
                    ),
                    ft.FilledButton(
                        text = 'Botão1',
                        # style = ft.ButtonStyle(
                        #     bgcolor = ft.colors.ON_PRIMARY,
                        #     color = ft.colors.ON_INVERSE_SURFACE
                        # )
                        # ,
                    ),
                    # ft.FilledButton(
                    #     text = 'Botão2',
                    #     style = ft.ButtonStyle(
                    #         bgcolor = ft.colors.ON_SECONDARY,
                    #         color = ft.colors.ON_INVERSE_SURFACE
                    #     )
                    #     ,
                    # ),
                    # ft.FilledButton(
                    #     text = 'Botão3',
                    #     style = ft.ButtonStyle(
                    #         bgcolor = ft.colors.ON_TERTIARY,
                    #         color = ft.colors.ON_INVERSE_SURFACE
                    #     )
                    #     ,
                    # ),                                        
                    ft.FilledTonalButton(
                        text = 'FilledTonalButton'
                    ),
                    ft.OutlinedButton(
                        text = 'OutlinedButton'
                    ),
                    ft.TextField('ksajgh',label='texto', 
                                filled=True, dense = True,
            
                                ),
                    ft.Dropdown(label='drop', 
                                options=[ft.dropdown.Option(i) for i in range(10)],
                                dense = True,
                                filled = True,
                                # color = ft.colors.ON_PRIMARY,
                                # fill_color =ft.colors.,
                                # text_style = ft.TextStyle(
                                #     color=ft.colors.PRIMARY,
                                # )
                                # bgcolor = 'black,0.7',
                    ),
                    ft.Slider(
                        min = 1,
                        max = 100,
                        divisions = 100,
                        label='casa',
                        value=50,

                    ),
                    ft.Switch(label = 'valor swith') ,
                    ft.Checkbox(label ='checkbox'),
                    ft.Icon(name = ft.icons.BOOK),
                    ft.PopupMenuButton(
                        content=ft.Text('TEMA', weight=ft.FontWeight.W_900),
                        items = [
                            ft.PopupMenuItem('dark',checked=False),
                            ft.PopupMenuItem('light',checked=True ),
                        ],
                    ),   
                    ft.Text('título',
                            color=ft.colors.PRIMARY,
                            
                    ),              
                    

                ],
                
                columns={'xs':48, 'sm':60 },
                spacing = 0,
                run_spacing = 10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,            

            )
        )

        self.cts = [self.ferramentas, self.tema_escolhido, self.select_dark_light,]


           

        self.cts += [self.menus[i] for i in self.atributos_ColorScheme]
        
        self.cts += [ft.ResponsiveRow([self.btn_save, self.linha_salve], columns=96, spacing=0, run_spacing=0)]
    
        return ft.ResponsiveRow(self.cts,
                           columns={'xs':2, 'sm':3 },
                           spacing=20,
                        #    expand = True,
                           run_spacing = 0,
                           
            )

    def GerarCores(self, data):
        return ft.GridView(
            [
                # ft.IconButton(icon = ft.icons.SQUARE, icon_color = i, col = 0.2,splash_radius=0, padding = 0, on_focus=self.SelecColor) 
                ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor ) 
                for i in ft.colors.colors_list[ft.colors.colors_list.index('scrim')+1:]
            ],
            col = 2, 
            # columns=5,
            width=200,
            height=100,
            runs_count = 8,
            padding = 0,
            # aspect_ratio=1,
            run_spacing=0, 
            spacing=0
        )        



    def TornarVizivel(self, e):
        self.btn_save.visible = False
        self.linha_salve.visible = True
        self.linha_salve.update()
        self.btn_save.update()


    def Salvar(self, e):
        nome_tema = self.nome_tema.value
        if nome_tema not in ['', ' ', None]+list(self.arquiv.keys()):
            self.arquiv[nome_tema] = self.dic_atributos
            self.escrever_json(self.arquiv, self.arquivo_temas)
            self.linha_salve.visible = False
            self.btn_save.visible = True
        else:
            self.nome_tema.hint_text = 'Digite um nome de Tema válido ou clique em Cancelar'
            # self.nome_tema.hint_style = ft.TextStyle(size = 10)

        e.page.update()


    def CarregarTema(self, e):
        tema = self.tema_escolhido.value
        if tema:
            e.page.bgcolor = 'surface'

            self.dic_atributos = self.arquiv[tema].copy()
            # print(self.dic_atributos["surface"])
        #     cores_claras = ["white","deeppurple","indigo","lightblue","lightgreen","lime"
        # "yellow","bluegrey","grey"]
        #     cc = []
        #     for i in cores_claras:
        #         cc.extend([f"{i}{j}" for j in range(100, 600,100)])
        #     cores_claras += cc
        #     if self.dic_atributos["surface"] in cores_claras:
        #         e.page.theme_mode = ft.ThemeMode.LIGHT
        #     else:
        #         e.page.theme_mode = ft.ThemeMode.DARK

      

            if self.dic_atributos.get("light", False):
                e.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                e.page.theme_mode = ft.ThemeMode.DARK


            e.page.theme = ft.Theme(
                color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
                color_scheme=ft.ColorScheme(
                    primary = self.dic_atributos["primary"],
                    on_primary = self.dic_atributos["on_primary"],
                    on_secondary_container = self.dic_atributos["on_secondary_container"],
                    outline = self.dic_atributos["outline"],
                    shadow = self.dic_atributos["shadow"],
                    on_surface_variant = self.dic_atributos["on_surface_variant"],
                    surface_variant = self.dic_atributos["surface_variant"],
                    primary_container = self.dic_atributos["primary_container"],
                    on_surface = self.dic_atributos["on_surface"],
                    surface = self.dic_atributos["surface"],
                    # on_primary_container = self.dic_atributos["on_primary_container"],
                    # secondary = self.dic_atributos["secondary"],
                    # on_secondary = self.dic_atributos["on_secondary"],
                    # tertiary = self.dic_atributos["tertiary"],
                    # on_tertiary = self.dic_atributos["on_tertiary"],
                    # tertiary_container = self.dic_atributos["tertiary_container"],
                    # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                    # error = self.dic_atributos["error"],
                    # on_error = self.dic_atributos["on_error"],
                    # error_container = self.dic_atributos["error_container"],
                    # on_error_container = self.dic_atributos["on_error_container"],
                    # background = self.dic_atributos["background"],
                    # on_background = self.dic_atributos["on_background"],
                    # outline_variant = self.dic_atributos["outline_variant"],
                    # scrim = self.dic_atributos["scrim"],
                    # inverse_surface = self.dic_atributos["inverse_surface"],
                    # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                    # inverse_primary = self.dic_atributos["inverse_primary"],
                    # surface_tint = self.dic_atributos["surface_tint"],
                )
            )
                
            for i in list(self.dic_atributos.keys()):
            #     self.icones[i].color = self.dic_atributos[i]
                try:
                    self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
                except:
                    pass
            # self.menus[i].update()  

            with open('mytheme.txt', 'w') as arq:
                arq.write(tema)

            # self.icones[i].update()                
            e.page.update()
            
    def Cancelar(self, e):
        self.nome_tema.clean()
        self.linha_salve.visible = False
        self.btn_save.visible = True
        self.update()

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}


    def definirCor(self, e):
        # print('bgcolor = ',e.control.bgcolor,'---', 'data =',e.control.data )
        # self.icones[e.control.data].color = e.control.bgcolor
        # self.icones[e.control.data].data[1] = True
        # self.icones[e.control.data].update()

        self.menus[e.control.data].content.border = ft.border.all(5,e.control.bgcolor)
        self.menus[e.control.data].update()

        if e.control.data == 'surface':
            self.page.bgcolor = e.control.bgcolor

        # for i in self.atributos_ColorScheme:
        #     if self.icones[i].data[1] and self.icones[i].data[0] == e.control.data:
        #         self.dic_atributos[i] = e.control.bgcolor


        self.dic_atributos[e.control.data] = e.control.bgcolor


        self.page.theme = ft.Theme(
            color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
            color_scheme=ft.ColorScheme(
                primary = self.dic_atributos["primary"],
                on_primary = self.dic_atributos["on_primary"],
                on_secondary_container = self.dic_atributos["on_secondary_container"],
                outline = self.dic_atributos["outline"],
                shadow = self.dic_atributos["shadow"],
                on_surface_variant = self.dic_atributos["on_surface_variant"],
                surface_variant = self.dic_atributos["surface_variant"],
                primary_container = self.dic_atributos["primary_container"],
                on_surface = self.dic_atributos["on_surface"],
                surface = self.dic_atributos["surface"],
                # on_primary_container = self.dic_atributos["on_primary_container"],
                # secondary = self.dic_atributos["secondary"],
                # on_secondary = self.dic_atributos["on_secondary"],
                # tertiary = self.dic_atributos["tertiary"],
                # on_tertiary = self.dic_atributos["on_tertiary"],
                # tertiary_container = self.dic_atributos["tertiary_container"],
                # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                # error = self.dic_atributos["error"],
                # on_error = self.dic_atributos["on_error"],
                # error_container = self.dic_atributos["error_container"],
                # on_error_container = self.dic_atributos["on_error_container"],
                # background = self.dic_atributos["background"],
                # on_background = self.dic_atributos["on_background"],
                # outline_variant = self.dic_atributos["outline_variant"],
                # scrim = self.dic_atributos["scrim"],
                # inverse_surface = self.dic_atributos["inverse_surface"],
                # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                # inverse_primary = self.dic_atributos["inverse_primary"],
                # surface_tint = self.dic_atributos["surface_tint"],
            )
        )

        self.page.update()

    def paleta(self, data):
        return ft.GridView(
            [
                ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor) 
                for i in self.cores
            ],
            col = 2, 
            
            runs_count = 6,
            padding = 0,
            # aspect_ratio=16/9,
            run_spacing=0, 
            spacing=0
        )

    def Atributos(self, classe):
        return [attr for attr in dir(classe) if not attr.startswith('__')]




class SelecionarData(ft.Row):
    def __init__(self, on_change = None):
        super().__init__() 
        self.on_change = on_change
        self.d = ft.DatePicker(
            cancel_text="Cancelar",
            confirm_text= 'Ok',
            error_format_text= 'Data inválida!',
            field_hint_text= 'MM/DD/YYYY',
            field_label_text= 'Digite uma data',
            help_text= 'Selecione uma data no calendário',
            date_picker_mode=ft.DatePickerMode.DAY,
            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR,
            value = datetime.date(2024,10,30),
            on_change = self.Change
        )
        # self.on_click = self.AbrirData
        self.tooltip = 'Selecionar data inicial'
        self.btn = ft.IconButton(
                icon=ft.icons.DATE_RANGE,
                on_click=lambda _: self.page.open(self.d),
        )

        self.controls = [
                self.btn,
                self.d
        ]

    def did_mount(self):
        self.page.overlay.append(self.d)

    def Change(self, e):
        if self.on_change:   
            e.valor = e.control.value.strftime("%d-%m-%Y")
            self.on_change(e)

    @property
    def value(self):
        return self.d.value.strftime("%d-%m-%Y")

    @value.setter
    def value(self, value):
        self.d.value = value
        self.update()



class TemaSelect(ft.PopupMenuButton):
    def __init__(self):
        super().__init__()
        
        class Cor:
            def __init__(self, principal, secundaria, terciaria, fundo,texto ):
                self.principal = principal
                self.secundaria = secundaria
                self.terciaria = terciaria
                self.cor_texto = texto
                self.fundo = fundo
        class PaletaDeCores:
            # Cores seguindo o padrão de contraste fornecido
            COR_001 = Cor("#ceb9b9", "#886969", "#654242", "#2b2424", "#000000")  # Branco, Rosa Claro, Marrom Escuro, Preto
            COR_002 = Cor("#29097d", "#4d3784", "#9c8bc9", "#2e3c15", "#ffffff")  # Branco Suave, Rosa Médio, Marrom Médio, Preto
            COR_003 = Cor("#004d00", "#007f00", "#66cc66", "#9c7e7e", "#ffffff")
        

            # Mantendo as demais cores ou modificando conforme necessário
            COR_004 = Cor("#7d0000", "#9c2b2b", "#d94747", "#4e5d33", "#ffffff")  # Laranja Claro, Coral, Tomate, Cinza Ardósia Escuro
            COR_005 = Cor("#7d3d00", "#b64d00", "#ff7f00", "#422667", "#ffffff")  # Roxo Lavanda, Cardo, Ameixa, Preto
            COR_006 = Cor("#3b2b2b", "#7d4a4a", "#b56e6e", "#000000", "#ffffff")  # Verde Limão, Verde, Verde Grama, Índigo
            COR_007 = Cor("#4d4d4d", "#7f7f7f", "#b3b3b3", "#4c2828", "#000000")  # Azul Turquesa, Turquesa Médio, Verde Mar, Marrom Saddle
            COR_008 = Cor("#FFD700", "#FFA500", "#FF8C00", "#4b2878", "#000000")  # Ouro, Laranja, Laranja Escuro, Azul Marinho
            COR_009 = Cor("#1a1a1a", "#333333", "#666666", "#9c7e7e", "#ffffff")  # Laranja Vermelho, Tomate, Coral, Cinza Ardósia Escuro
        self.tooltip = ''
        # self.content = ft.Container(
        #     ft.Text('Tema', weight='BOLD'), 
        #     bgcolor='#864949',
        #     border_radius=8,
        #     padding=ft.Padding(8,0,8,0)
        # )
        self.content = ft.Icon(name = ft.icons.PALETTE)
        self.splash_radius = 0
        self.items=[
            ft.PopupMenuItem(
            #     content = ft.Container(bgcolor = i.principal, width=200, height=20),
            #     height = 10,padding = 0,
            #     )
            # for i in self.Atributos2(PaletaDeCores)
                content = ft.GridView(
                    [
                        ft.Container(bgcolor = i.principal, data = i,col = 0.2, padding = 20, on_click=self.SelecColor,  ) 
                        for i in self.Atributos2(PaletaDeCores)
                    ],
                    # col = 2, 
                    # columns=5,
                    runs_count = 3,
                    padding = 0,
                    # aspect_ratio=1,
                    run_spacing=0, 
                    spacing=0
                )
            )
        ]

    def did_mount(self):
        def LerTema():
            try:
                with open('tema.txt', 'r') as arq:
                    tema = arq.read()
                
                return tema.split('\n')[:-1]
            except:
                return "#ceb9b9", "#886969", "#654242", "#2b2424", "#000000"
            
        cor1,cor2,cor3,cor_fundo,cor_texto = LerTema()
    
        self.page.theme = ft.Theme(
            color_scheme_seed = cor1,
            color_scheme = ft.ColorScheme(
                on_primary = cor1,
                on_secondary = cor2,
                on_tertiary = cor3,
                scrim = cor_fundo,
                on_inverse_surface=cor_texto,
                shadow = cor1, # cor das sombras"
                on_surface_variant = cor1, #cor dos labels e chekbox
                surface_variant = cor3, #cor do slider e cor de fundo do texfield",
                primary_container = cor1, #cor da bolinha do switch",
                on_surface = cor3, #cor HOVERED do checkbox",




                surface = cor3,
                on_primary_container = cor3,
                secondary = cor3,
                tertiary = cor3,
                tertiary_container = cor3,
                on_tertiary_container = cor3,
                error = cor3,
                on_error = cor3,
                error_container = cor3,
                on_error_container = cor3,
                background = cor3,
                on_background = cor3,
                outline_variant = cor3,
                inverse_surface = cor3,
                inverse_primary = cor3,
                surface_tint = cor3,       



            ),
            text_theme = ft.TextTheme(
                body_medium=ft.TextStyle(
                    size = 15,
                    weight=ft.FontWeight.W_500,
                )
            ),  
            slider_theme=ft.SliderTheme(
                    thumb_color = cor1,
            ),                                
            switch_theme= ft.SwitchTheme(
                thumb_color = {
                    ft.ControlState.DEFAULT:cor1,
                    ft.ControlState.HOVERED:None,
                    ft.ControlState.SELECTED:cor3,

                },
                track_color = {
                    ft.ControlState.DEFAULT:cor2,
                    ft.ControlState.HOVERED:cor2,
                    

                },
                overlay_color = {
                    ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                    ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
                },
                track_outline_color= {
                    ft.ControlState.DEFAULT:cor1,
                    ft.ControlState.HOVERED:cor1,
                },
                track_outline_width= {
                    ft.ControlState.DEFAULT:0,
                    ft.ControlState.HOVERED:0
                },
            ),
            checkbox_theme = ft.CheckboxTheme(
                overlay_color = {
                    ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                    ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
                },  
                # fill_color = {
                #     ft.ControlState.DEFAULT:self.cor_fundo,
                #     ft.ControlState.HOVERED:self.cor_fundo,
                # }, 
                # border_side = ft.BorderSide(1,self.cor1),                           
            ),
            # primary_color= self.cor,
            # primary_color_dark= self.cor,
            # primary_color_light= self.cor, 
            # icon_theme = ft.IconTheme(
            #     color = cor1, 
            #     ),
        )
        self.page.bgcolor = ft.colors.SCRIM
        self.page.update()
  

    def SelecColor(self, e):
        self.cor1 = e.control.data.principal
        self.cor2 = e.control.data.secundaria
        self.cor3 = e.control.data.terciaria
        self.cor_texto = e.control.data.cor_texto
        self.cor_fundo = e.control.data.fundo
        # print(self.cor1, self.cor2, self.cor3, self.cor_fundo)

        self.page.theme = ft.Theme(
            color_scheme_seed = self.cor1,
            color_scheme = ft.ColorScheme(
                on_primary = self.cor1,
                on_secondary = self.cor2,
                on_tertiary = self.cor3,
                scrim = self.cor_fundo,
                on_inverse_surface=self.cor_texto,
                shadow = self.cor1, # cor das sombras"
                on_surface_variant = self.cor1, #cor dos labels e chekbox
                surface_variant = self.cor3, #cor do slider e cor de fundo do texfield",
                primary_container = self.cor1, #cor da bolinha do switch",
                on_surface = self.cor3, #cor HOVERED do checkbox",




                surface = self.cor3,
                on_primary_container = self.cor3,
                secondary = self.cor3,
                tertiary = self.cor3,
                tertiary_container = self.cor3,
                on_tertiary_container = self.cor3,
                error = self.cor3,
                on_error = self.cor3,
                error_container = self.cor3,
                on_error_container = self.cor3,
                background = self.cor3,
                on_background = self.cor3,
                outline_variant = self.cor3,
                inverse_surface = self.cor3,
                inverse_primary = self.cor3,
                surface_tint = self.cor3,       



            ),
            text_theme = ft.TextTheme(
                body_medium=ft.TextStyle(
                    size = 15,
                    weight=ft.FontWeight.W_500,
                )
            ),  
            slider_theme=ft.SliderTheme(
                    thumb_color = self.cor1,
            ),                                
            switch_theme= ft.SwitchTheme(
                thumb_color = {
                    ft.ControlState.DEFAULT:self.cor1,
                    ft.ControlState.HOVERED:None,
                    ft.ControlState.SELECTED:self.cor3,

                },
                track_color = {
                    ft.ControlState.DEFAULT:self.cor2,
                    ft.ControlState.HOVERED:self.cor2,
                 

                },
                overlay_color = {
                    ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                    ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
                },
                track_outline_color= {
                    ft.ControlState.DEFAULT:self.cor1,
                    ft.ControlState.HOVERED:self.cor1,
                },
                track_outline_width= {
                    ft.ControlState.DEFAULT:0,
                    ft.ControlState.HOVERED:0
                },
            ),
            checkbox_theme = ft.CheckboxTheme(
                overlay_color = {
                    ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                    ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
                },  
                # fill_color = {
                #     ft.ControlState.DEFAULT:self.cor_fundo,
                #     ft.ControlState.HOVERED:self.cor_fundo,
                # }, 
                # border_side = ft.BorderSide(1,self.cor1),                           
            ),
            # primary_color= self.cor,
            # primary_color_dark= self.cor,
            # primary_color_light= self.cor, 
            # icon_theme = ft.IconTheme(
            #    color = self.cor1, 
            # ),
        )
        
        # self.cor_selecionada.value = f'Cor selecionada {self.cor1}'
        self.page.bgcolor = ft.colors.SCRIM
        self.Salvar(e)
        self.page.update()

    def Atributos(self, classe):
        return [attr for attr in dir(classe) if not attr.startswith('__')]

    def ChangeTema(self, e):
        tema = e.control.text
        if tema == 'dark':
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        self.nome_tema.value = tema
        self.page.update()        

    def ChangeVisual(self, e):
        tema = e.control.text
        self.page.theme = ft.Theme(
            visual_density = tema,            
        )
        self.Visual_density.value = tema
        self.page.update()

    def AtributosDaClasse(self, classe):
        # Obtendo a assinatura do método __init__ da classe
        init_params = inspect.signature(classe.__init__).parameters
        # Retornando os nomes dos parâmetros, excluindo 'self'
        return [param for param in init_params if param != 'self']

    def Atributos2(self, classe):
        # Retorna uma lista dos atributos da classe que não começam com '__'
        return [getattr(classe, attr) for attr in dir(classe) if not attr.startswith('__')]


    def Salvar(self, e):
        cores_tema = self.cor1,self.cor2,self.cor3,self.cor_fundo,self.cor_texto
        print(cores_tema)
        with open('tema.txt', 'w') as arq:
            for i in cores_tema:
                arq.write(f'{i}\n')




class PopMenu(ft.Container):
    def __init__(self,nome, content):
        super().__init__()
        self.content2 = content
        self.expand = False
        self.padding=ft.Padding(8,0,8,0)
        self.margin = ft.Margin(2,0,2,0)
        self.on_click = self.Diag
        self.border_radius = 8
        self.bgcolor = ft.colors.SECONDARY_CONTAINER
        self.content = ft.Text(nome)

    def Diag(self,e):     
        dialog = ft.AlertDialog(
            content=self.content2,
            bgcolor = ft.colors.TRANSPARENT,
            inset_padding = 0,
            shadow_color = ft.colors.TRANSPARENT,
            surface_tint_color = ft.colors.TRANSPARENT,            

        )        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()




class TabButton(ft.Container):
    def __init__(self,
                 text1,
                 text2,
                 controls1, #list[controls]
                 controls2, #list[controls]
        ):
        super().__init__()
        self.text1 = text1
        self.text2 = text2
        self.height = None
        self.bgcolor = None
        
        # self.expand = True
        self.border_radius = 8
        self.padding = 4
        self.columns = 12
        self.alignment = ft.alignment.top_center
        self.controls1 = controls1
        self.controls2 = controls2
        self.style=ft.ButtonStyle(
            padding=ft.Padding(6,0,6,0)
        )
        self.textoclic = ft.Container(
            content = ft.Text(
                value = self.text1, 
                style=ft.TextThemeStyle.BODY_LARGE, 
                weight=ft.FontWeight.W_700,
                col = 12, 
                expand_loose=True,
                text_align=ft.TextAlign.CENTER ,
            ),
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            border_radius=8,

        )
        self.textoclic = ft.FilledTonalButton(
            text = self.text1,
            style=self.style,
            height = 20,
            data = True,
            on_click=self.Changetabs
        )

        self.modoexibido = ft.ResponsiveRow(
            columns=self.columns,
            controls = [self.textoclic]+self.controls1,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            # expand=True,
        )

        self.content = self.modoexibido
                  
    def Changetabs(self,e):
        e.control.data = not e.control.data
        if e.control.data:
            e.control.text = self.text1
            self.textoclic.text = self.text1
            self.modoexibido.controls = [self.textoclic]+self.controls1
            # self.modos.height = 260

        else:
            e.control.text = self.text2
            self.textoclic.text = self.text2
            self.modoexibido.controls = [self.textoclic]+self.controls2
            # self.modos.height = 260

        e.control.update()
        self.modoexibido.update()




class BotaoCT(ft.Container):
    def __init__(self,nome,on_click = None, bgcolor = None, scale = None, text_size = None, col = None, data = None):
        super().__init__()
        self.on_click=on_click
        self.border_radius = 10
        self.bgcolor = bgcolor
        self.data = data
        self.scale = scale
        self.col = col
        self.text_size = text_size
        self.expand = False
        self.border = ft.border.all(1,ft.colors.WHITE70)
        self.margin = ft.Margin(2,0,2,0)
        self.padding = ft.Padding(0,2,0,2)
        self.on_hover = self.Status
        # self.border=ft.Border(right=ft.BorderSide(2,'white,0.4'))
        self._nome = nome
        # self.content = ft.Row([ft.VerticalDivider(color='blue', width=2), ft.Text(nome, weight='BOLD', text_align='center'),ft.VerticalDivider(color='blue', width=2),],alignment='center')
        self.content = ft.Text(self._nome, weight='BOLD', text_align='center', size = self.text_size , color = "white,0.7")

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome):
        self._nome = nome
        self.content = ft.Text(self._nome, weight='BOLD', text_align='center', size = self.text_size )
        self.update()
 
    def Status(self, e):
        self.content.color =  "blue" if e.data == "true" else "white,0.7"
        self.update()

    
class My_tabelaC(ft.Column):
    def __init__(self, dic,# dicionário
                 larguras = None, #dict
                 largura_default = 60
                    ):
        super().__init__()
        self.spacing = 5
        self.run_spacing = 5
        self._dic = dic 
        self.visible = False 
        self.largura_default = largura_default
        self._larguras = larguras
        if self._larguras is None:
            self._larguras = {}

        self.Iniciar()     
        self.Linhas()


    def Larg(self,coluna):
        if not self._larguras is None:
            return  self._larguras.get(coluna,self.largura_default)
        else:
            return self.largura_default

    def Iniciar(self):
        self.chaves = list(self._dic.keys())
        # if self._larguras is None:
        #     self._larguras = {i:60 for i in self.chaves}
        self.opcoes = self._dic[self.chaves[0]]


    def Colunas(self):
        self.controls = [ft.Container(ft.Row([ft.Text(self.chaves[0], width=self.Larg(self.chaves[0]), text_align='end', weight='BOLD')]+
                        [ft.Text(i, width=self.Larg(i), text_align='center', weight='BOLD') for i in self.chaves[1:]], tight=True),bgcolor='white,0.3')]

            
        
    def Linhas(self):
        self.Colunas()
        for i, k in enumerate(self._dic[self.chaves[0]]):     
            cor  = 'black' if i%2 == 0 else  'white,0.03'  
            self.controls.append(
                ft.Container(ft.Row([
                                Display(value = self._dic[self.chaves[0]][i],opitions=self.opcoes, width=self.Larg(self.chaves[0]),height=20,text_size = 12, 
                                        borda_width = 0,border_radius = 0, 
                                                text_align= ft.TextAlign.CENTER, horizontal_alignment=ft.CrossAxisAlignment.END, bgcolor = 'white,0')
                ]+[ft.Text(self._dic[j][i],width=self.Larg(j), text_align='center') for j in self.chaves[1:]], tight=True),bgcolor=cor)
                
                )
        
            
    def Atualizar(self):
        try:
            self.update()
        except:
            pass


    @property
    def dic(self):
        return self._dic
    
    @dic.setter
    def dic(self, dic):
        if isinstance(dic, dict):
            self._dic = dic
            # self._larguras = None
            self.Iniciar()
            self.Linhas()
        self.Atualizar()

    @property
    def larguras(self):
        return self._larguras
    
    @larguras.setter
    def larguras(self,  valor = ('chave','valor')):        
        if valor[0] in self.chaves and isinstance(valor[1], int):
            # self.Iniciar()
            self._larguras[valor[0]] = valor[1]
            # print('aceitou')
        else:
            print('chave ou valor inválido')
        self.Linhas()
        self.Atualizar()


class Slider_quad(ft.Container):
    def __init__(self, 
                 min = 0,
                 max = 100,
                 value = 0,
                 width = 200,
                 height = 20,
                 data = None,
                 on_change = None,
                 tooltip = None,
                 bgcolor = None,
                 border_color = None,
                 col = None,
                 text_size = 18,
                 text_width = 60

        ):
        super().__init__()
        self.height = height
        self.width = width
        self.scale = 0.8
        self._value = value
        self.min = min
        self.max = max
        self.data = data
        self.on_change = on_change
        self.tooltip = tooltip
        self.bgcolor = bgcolor
        self.col = col
        self.text_size = text_size
        self.text_width = text_width
        self.maxx = self.width-self.text_width
        
        self.border_color = border_color
        if self.border_color is None:
            self.border_color  = 'white,0.5'

        self.border = ft.border.only(ft.BorderSide(0.1,self.border_color),ft.BorderSide(0.1,self.border_color),ft.BorderSide(1,self.border_color),ft.BorderSide(1,self.border_color))
        # self.gesto = Gestos('caixa', movimento_vertical=False, width=self.width-190, func=self.Arrastou)
        # self.gesto.Add_control('campo',ft.Container(content = ft.Text(value = self.gesto.value),bgcolor='white,0.15', width=50, height=self.height,border= self.border))


        self.gesto = ft.Stack()
        self.gesto.controls = [
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_vertical_drag_update=self.on_pan_update,  
                    left = round(self.map_value(self._value, in_min=self.min, in_max=self.max, out_min=0, out_max=self.maxx),2), 
                    top = 0,   
                    hover_interval = 0,
                    drag_interval = 50,                        
                    content= ft.Container(content = ft.Text(value = self._value, text_align='center', weight = 'BOLD', size =  self.text_size),bgcolor='white,0.15', width=60, height=self.height,border= self.border),
                    data = self.data,
                    on_double_tap = self.SetarValor
                )            
        ]
          
        self.content = self.gesto
        

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if isinstance(value, int) or isinstance(value, float):
            valor = round(float(value),2)
            if valor >= self.max:
                novo_valor = self.maxx
                novo_texto = self.max
            elif valor <= self.min:
                novo_valor = 0
                novo_texto = self.min
            else:
                y = self.map_value(valor, in_min=self.min, in_max=self.max, out_min=0, out_max=self.maxx)
                novo_valor = round(y,2)
                novo_texto = valor
            self.gesto.controls[0].left = novo_valor
            self.gesto.controls[0].content.content.value = novo_texto
            self.Atualizar()                
            
 

    def Atualizar(self):
        try:
            self.update()
        except:
            pass
    def map_value(self, x, in_min=0, in_max=300, out_min=5, out_max=120):
        return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)
    def on_pan_update(self, e: ft.DragUpdateEvent):
        # if self.movimento_vertical:
        #     e.control.top = max(0, e.control.top + e.delta_y)
        # print('casa')
        e.control.left = max(0, e.control.left + e.delta_x)
        
        if e.control.left >= self.maxx:
            e.control.left = self.maxx
        if self.height and e.control.top >= self.height:
            e.control.top = self.height -100 
        # print(e.control.left)     
        # self._value = (e.control.left, e.control.top)
        
        x = e.control.left
        y = self.map_value(x, in_min=0, in_max=self.maxx, out_min=self.min, out_max=self.max)
        novo_valor = round(y,2)
        e.control.content.content.value = novo_valor
        # e.control.update()
        self._value = novo_valor

        if not self.on_change is None:
            self.on_change(e)
        self.Atualizar()
    def Voltar(self,e):
            valor = round(float(e.control.value),2)
            if valor >= self.max:
                novo_valor = self.maxx
                novo_texto = self.max
            elif valor <= self.min:
                novo_valor = 0
                novo_texto = self.min
            else:
                y = self.map_value(valor, in_min=self.min, in_max=self.max, out_min=0, out_max=self.maxx)
                novo_valor = round(y,2)
                novo_texto = valor

            self.gesto.controls[0].left = novo_valor
            self.gesto.controls[0].content.content = ft.Text(value = novo_texto, text_align='center', weight = 'BOLD')
            self._value = valor
            self.Atualizar()

    def SetarValor(self, e):        
        e.control.content.content = ft.TextField(dense = True,  text_size = 9, border=None,border_width = 0,expand=True,  on_submit= self.Voltar)
        self.Atualizar()

class Criar_exe:
    def __init__(self,
        programas = [
            'main.py',
            'tabela_mandados.py',
            'rpv_federal.py',
            'automacoes_flet.py',
            'mesclarpdfplanilha.py',
            'precatorios_flet.py',
            'visualizar_dados_prec.py'

            ], 
            arquivos = None                
    ):
        

        if not arquivos is None:
            def Criar(i):
                PyInstaller.__main__.run([
                    i,
                    '--onefile',
                    '--windowed',
                    f'--add-data "{arquivos}"'
                        ])
        else:
            def Criar(i):
                PyInstaller.__main__.run([
                        i,
                        '--onefile',
                        '--windowed'
                    ])            
            
        self.limpar_pasta('build')
        
        for i in programas:
            # if not i.endswith('.spec') and i.endswith('.py'):
            sp = i.split('.')[0]+'.spec'
            if  os.path.exists(sp):
                PyInstaller.__main__.run([
                    sp
                ])  
            elif i.endswith('.py'):
                Criar(i)

            self.limpar_pasta('build')

    def limpar_pasta(self, pasta):
        try:
            rmtree(pasta)
            print(f"A pasta '{pasta}' foi deletada com sucesso.")
        except OSError as e:
            print(f"Erro ao deletar a pasta: {e}")
          

class Classificador(ft.Container):
    def __init__(self,
                 value = 'valor',
                 func = None,
                 width = None,
                height = None,
                theme_style = ft.TextThemeStyle.TITLE_MEDIUM,
                color = None,
                data = None
                 ):
        super().__init__()
        # self.tight=True
        # self.spacing=0
        # self.height=200
        # self.run_spacing=0  
        # self.width =  width
        self.height = height
        self.theme_style = theme_style
        self.color = color
        self.value = value    
        self.func = func
        self.data = data
        self.seta = False
        self.icone = ft.Icon(ft.icons.ARROW_UPWARD, visible=False, size = 13)
        self.texto =  ft.Text(
                    self.value,
                    # spans = [ft.TextSpan(self.value),ft.TextSpan(style = ft.TextStyle(weight = 'BOLD', size = 20))], 
                    theme_style=self.theme_style,
                    color = self.color,
                    width = width,
                    text_align = 'center',
                )
                    
        self.texto2 = ft.Text(data = True, color = ft.colors.CYAN,style = ft.TextStyle(weight = 'BOLD', size = 20))
        self.content =  ft.Row(
            [
               self.texto,self.texto2
                # self.icone
            ], 
            width=width+20 if not width is None else None, 
            alignment='center',
            vertical_alignment='center',
            spacing=0,
            run_spacing=0,
        )
        self.on_click=self.Clicou
   

    def Clicou(self, e):
        self.seta = not self.seta
        # self.icone.visible = True
        # if self.seta:
        #     self.icone.name = ft.icons.ARROW_DOWNWARD
        # else:
        #     self.icone.name = ft.icons.ARROW_UPWARD

        self.texto2.data = not self.texto2.data
        if self.seta:
            self.texto2.value = "↑"
        else:
            self.texto2.value = "↓"

        if not self.func is None:
            self.func(e)
        try:
            self.update()
        except:
            pass


class Display(ft.Container):
    def __init__(self,
                 #adicionar clique duplo para abrit campo de txto
            data = None,
            value = None,
            opitions = None, #lista
            height =40,
            width = 120, 
            bgcolor = 'black' ,
            tipos_dados: Union[float, int, str] = [int, float],
            borda_width = 4,
            text_size = 25,
            border_radius = 10,
            func = None,
            on_click = None,
            text_color = None,
            text_align = 'center', #Optional[TextAlign] = None,
            horizontal_alignment = 'center', #CrossAxisAlignment 
            col = None,
            margin = None,
            border_color = ft.colors.with_opacity(0.2,ft.colors.PRIMARY),         
        ): 
        super().__init__()
        self.opitions = opitions
        self.func = func
        self.on_click = on_click
        self.data = data
        if self.opitions is None:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in range(30,250,1)]
        else:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in opitions]

        self.border_radius =border_radius
        self.borda_width = borda_width
        self.text_size = text_size
        if borda_width > 0:
            self.border = ft.border.all(self.borda_width, border_color)
        else:
            self.border = None
        self.data = data
        self._value = value
        self.bgcolor = bgcolor
        self.height =height
        self.width = width
        self.tipos_dados = tipos_dados
        self.text_align = text_align
        self.horizontal_alignment = horizontal_alignment         
        self._campotexto = ft.TextField(dense=True, on_submit=self.SetarValue)
        self.on_long_press = self.VirarCampoTexto
        self.col = col
        self.margin = margin
        self.GerarContent()

    def GerarContent(self):
        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = 'white', weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER
        )        

    def SetarValue(self,e):
        self._value = self._campotexto.value
        self.GerarContent()
        if not self.func is None:
            self.func(self._value)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()     

    def VirarCampoTexto(self,e):
        content_antigo = self.content
        self.content = self._campotexto
        if not self.on_click is None:
            self.on_click(e)  
        self.Atualizar()
     
    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, cor):
        self._text_color = cor  
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }        

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,        
        )
         
        self.Atualizar()




    def Clicou(self,e):
        if type(e.control.text) in [int, float]:
            valor = round(e.control.text,1)
        else:
           valor = e.control.text 
        self.content.content.controls[0].value = valor
        self._value = valor

        if not self.func is None:
            self.func(valor)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()



    @property
    def value(self):
        try:
            v = int(self._value)
        except:
            try:
                v = float(self._value)
            except:            
                v = self._value
        return v



    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    @value.setter
    def value(self, valor):
        if isinstance(self.content, ft.PopupMenuButton):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.items.append(ft.PopupMenuItem(valor, on_click = self.Clicou))
                self.content.content.controls[0].value = valor
                self.Atualizar()
            else:
                print('número inválido')
        elif isinstance(self.content, ft.TextField):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.value = valor
                self.Atualizar()
            else:
                print('número inválido')
 

class Verificar_pasta:
    def __init__(self,pastalocal = 'tabelamandadostjse'):
        self.pastalocal = pastalocal
        self.verificar_pasta()

    def verificar_pasta(self):
        user_profile = os.environ.get('USERPROFILE')
        # print(user_profile)
        if not user_profile:
            # return False  # USERPROFILE não está definido
            self.local = None

        caminho = os.path.join(user_profile, self.pastalocal)
        
        if os.path.exists(caminho):
            self.local = caminho
            # return self.caminho
        else:
            os.mkdir(caminho)
            # print(caminho)
            if os.path.exists(caminho):
                self.local = caminho
                # return self.caminho
            # else:
                # return None
    

    def caminho(self, nome):
        # self.verificar_pasta()
        return os.path.join(self.local, nome)


def verificar_pasta(pasta = 'tabelamandadostjse'):
    user_profile = os.environ.get('USERPROFILE')
    # print(user_profile)
    if not user_profile:
        return False  # USERPROFILE não está definido

    caminho = os.path.join(user_profile, pasta)
    
    if os.path.exists(caminho):
        # print(caminho)
        return caminho
    else:
        os.mkdir(caminho)
        # print(caminho)
        if os.path.exists(caminho):
            # print(caminho)
            return caminho
        else:
            return None

class TextField(ft.TextField):
    def __init__(self,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None, #125,
        height: OptionalNumber = None, #35,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # FormField specific
        #
        text_size: OptionalNumber = 15,
        text_style: Optional[TextStyle] = None,
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        icon: Optional[str] = None,
        border: Optional[InputBorder] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = 'white,0.3',
        border_radius: BorderRadiusValue = None,
        border_width: OptionalNumber = 0.9,
        border_color: Optional[str] = 'white,0.3',
        focused_color: Optional[str] = None,
        focused_bgcolor: Optional[str] = None,
        focused_border_width: OptionalNumber = None,
        focused_border_color: Optional[str] = None,
        content_padding: PaddingValue = None, #4,
        dense: Optional[bool] = True,
        filled: Optional[bool] = None,
        hint_text: Optional[str] = None,
        hint_style: Optional[TextStyle] = None,
        helper_text: Optional[str] = None,
        helper_style: Optional[TextStyle] = None,
        counter_text: Optional[str] = None,
        counter_style: Optional[TextStyle] = None,
        error_text: Optional[str] = None,
        error_style: Optional[TextStyle] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        prefix_text: Optional[str] = None,
        prefix_style: Optional[TextStyle] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        suffix_text: Optional[str] = None,
        suffix_style: Optional[TextStyle] = None,
        #
        # TextField Specific
        #
        value: Optional[str] = None,
        keyboard_type: Optional[KeyboardType] = None,
        multiline: Optional[bool] = None,
        min_lines: Optional[int] = None,
        max_lines: Optional[int] = None,
        max_length: Optional[int] = None,
        password: Optional[bool] = None,
        can_reveal_password: Optional[bool] = None,
        read_only: Optional[bool] = None,
        shift_enter: Optional[bool] = None,
        text_align: Optional[TextAlign] = None,
        autofocus: Optional[bool] = None,
        capitalization: Optional[TextCapitalization] = None,
        autocorrect: Optional[bool] = None,
        enable_suggestions: Optional[bool] = None,
        smart_dashes_type: Optional[bool] = None,
        smart_quotes_type: Optional[bool] = None,
        cursor_color: Optional[str] = None,
        cursor_width: OptionalNumber = None,
        cursor_height: OptionalNumber = None,
        cursor_radius: OptionalNumber = None,
        selection_color: Optional[str] = None,
        input_filter: Optional[InputFilter] = None,
        on_change=None,
        on_submit=None,
        on_focus=None,
        on_blur=None,
        ):    
       super().__init__(ref, key, width, height, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, text_size, text_style, label, label_style, icon, border, color, bgcolor, border_radius, border_width, border_color, focused_color, focused_bgcolor, focused_border_width, focused_border_color, content_padding, dense, filled, hint_text, hint_style, helper_text, helper_style, counter_text, counter_style, error_text, error_style, prefix, prefix_icon, prefix_text, prefix_style, suffix, suffix_icon, suffix_text, suffix_style, value, keyboard_type, multiline, min_lines, max_lines, max_length, password, can_reveal_password, read_only, shift_enter, text_align, autofocus, capitalization, autocorrect, enable_suggestions, smart_dashes_type, smart_quotes_type, cursor_color, cursor_width, cursor_height, cursor_radius, selection_color, input_filter, on_change, on_submit, on_focus, on_blur)


class Text(ft.Text):
    def __init__(self, 
        value: Optional[str] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # text-specific
        #
        spans: Optional[List[TextSpan]] = None,
        text_align: Optional[TextAlign] = None,
        font_family: Optional[str] = None,
        size: OptionalNumber = None,
        weight: Optional[FontWeight] = None,
        italic: Optional[bool] = None,
        style: Union[TextThemeStyle, TextStyle, None] = None,
        theme_style: Optional[TextThemeStyle] = None,
        max_lines: Optional[int] = None,
        overflow: Optional[TextOverflow] = None,
        selectable: Optional[bool] = None,
        no_wrap: Optional[bool] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        semantics_label: Optional[str] = None,
        ):                 
        super().__init__(value, ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, spans, text_align, font_family, size, weight, italic, style, theme_style, max_lines, overflow, selectable, no_wrap, color, bgcolor, semantics_label)
    

class Gestos(ft.Stack):
    def __init__(self,nome_json):
        super().__init__()
        self.nome_json = nome_json
        def colun(x=1):
            return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}
        self.expand=True
        self._movimento = True
        self.controls = []

    @property
    def movimento(self):
        return self._movimento
    
    @movimento.setter
    def movimento(self, movimento:bool):
        if isinstance(movimento, bool):            
            self._movimento = movimento
            if self._movimento:
                for i in self.controls:
                    i.on_vertical_drag_update = self.on_pan_update
                self.update()
        else:
            print(f'o valor dado para "movimento" não é booleano')


    def Add_control(self,nome, control ):
        self.arquiv = self.ler_json(self.nome_json, default={nome:{'left':0,'top':0}})
        try: 
            self.arquiv[nome] == 5
            
        except KeyError:
            self.arquiv[nome] = {'left':0,'top':0}
        self.escrever_json(self.arquiv,self.nome_json)

        if self._movimento:
            self.controls.append(
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_vertical_drag_update=self.on_pan_update if self._movimento else None,
                    
                    left=self.arquiv[nome]['left'],
                    top=self.arquiv[nome]['top'],               
                    content= control ,
                    data = nome
                )
            )
        else:
            try:
                control.left=self.arquiv[nome]['left']
                control.top=self.arquiv[nome]['top']              
                control.data = nome
                self.controls.append(control)
            except:
                self.controls.append(
                    ft.Column(
                        controls = [control],
                        left=self.arquiv[nome]['left'],
                        top=self.arquiv[nome]['top'],
                        data = nome   
                        )
                )
                
        


    def on_pan_update(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        self.arquiv[e.control.data]['left'] = e.control.left
        self.arquiv[e.control.data]['top'] = e.control.top
        self.escrever_json(self.arquiv,self.nome_json)
        e.control.update()
        

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}


class Tabe(ft.Tabs):
    def __init__(self,  funcao = None, *controls):
        super().__init__()
        self.selected_index=1
        self.animation_duration=3
        self.expand=1
        self.controls = list(controls)
        self.funcao = funcao
        self.on_change = self.func
        if isinstance(self.controls, list) and len(self.controls) >0:
            for i in self.controls: 
                if len(i) == 2:                
                    self.tabs.append(ft.Tab(icon=i[0],content=i[1] ))
                else:
                    self.tabs.append(ft.Tab(text=i[0],content=i[1] ))


    def Add(self, icone, janela):
        self.tabs.append(ft.Tab(icon=icone,content=janela ))
        try:
            self.update()
        except:
             pass

    def func(self,e):
        if self.funcao != None:
            self.funcao(e)
        # pass
  

class Atalhos:
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.pasta = verificar_pasta('tabelamandadostjse')
        self.abreviacoes = os.path.join(self.pasta,'abreviacoes.json')
        self.arq_abrev = self.ler_json(self.abreviacoes)
    def Aplicar_atalhos(self):
        kb.add_hotkey('capslock',self. Clic)

        for i,j in self.arq_abrev.items():
            kb.add_abbreviation(i, j)  
        kb.wait('shift+esc')
        kb.remove_all_hotkeys()               
    def Clic(self):
        # Obtém o estado atual do Caps Lock
        caps_lock_state = kb.is_pressed('caps lock')

        # Inverte o estado do Caps Lock
        kb.press_and_release('caps lock')

        # Restaura o estado anterior do Caps Lock
        if caps_lock_state:
            kb.press('caps lock')
        else:
            kb.release('caps lock')

        # Clique do mouse (pode ser ajustado conforme necessário)
        pyautogui.click()

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}


class Resize:
    def __init__(self,page, exibir = True):
        self.page = page
        self.page.on_resized = self.page_resize
        self.page.window.on_event = self.page_resize
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados()  

    def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        with open('assets/tamanho.txt', 'w') as arq:
            arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')

  

    def Ler_dados(self):
        try:
            with open('assets/tamanho.txt', 'r') as arq:
                po = arq.readline()
        except:
            with open('assets/tamanho.txt', 'w') as arq:
                arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
        po = po.split(',')
        po = [int(float(i)) for i in po]
        
        self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po


class Teclas:
    def __init__(self,page):
        self.page = page
        self.page.on_keyboard_event = self.Teclas
        self.tecla = None
        while self.tecla != 'enter':
            sleep(0.3)
    
    def Teclas(self, e: ft.KeyboardEvent):
        match e.key:
            case 'Enter':
                self.tecla = 'enter'
            # case 'Escape':
            #     self.tecla = 'esc'

class AtalhosTexto(ft.Column):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.abreviacao = ft.IconButton(icon=ft.icons.APP_SHORTCUT, 
                tooltip='criar atalho', on_click=self.CriarAbreviacao)
        # self.page.add(self.abreviacao)
        self.Editar = ft.IconButton(icon=ft.icons.SETTINGS, 
                tooltip='Editar atalhs', on_click=self.Editar_atalhos)


        self.scroll=ft.ScrollMode.ADAPTIVE
        self.height = 510
        self.auto_scroll=True
        self.info = f'''
ctrl+alt+a: cria uma abreviação
alt: botão do meio do mouse
capslock: clic
eee: enviar mandados
eeee: enviar mandados simplificado
config: configurar enviar mandado
ctrl+ç: baixar mandado
ctrl+/: baixar mandados
ctrl+]: Transferir mandado
cbcb: configurar transferir mandado
add: Adicionar novo contato à agenda do iphone (usando mouse)
addconfig: Configurar Adicionar novo contato à agenda do iphone (usando mouse)
inci: Iniciar navegador (selenium)
verific: Verificar contatos (selenium)
rasp: Raspar mandados
slenv: Enviar mandados(selenium)
slenvt: Enviar mandados(selenium) - apenas a mensagem
tttt: atualizar planilha dos mandados
testoff: Para enviar os mandados para os devidos contatos (selenium) (padrão)
teston: Para enviar os mandados para leanio moraes  (selenium)
tabel: para exibir a tela dos mandado a serem enviados
pppp: preparar PDFs dos mandados para impressão
'''
        


        self.Infos()

    def Aplicar_atalhos(self):
        kb.add_hotkey('capslock',self. Clic)

        # for i,j in ap.arq_abrev.items():
        #     self.kb.add_abbreviation(i, j)

        # # self.kb.add_abbreviation('f.', 'Fórum de Salgado')
        # # self.kb.add_abbreviation('F.', 'Fórum de Salgado')
        # # self.kb.add_abbreviation('e.', 'Expedi Mandados')
        # # self.kb.add_abbreviation('E.', 'Expedi Mandados')    
        kb.wait('shift+esc')
        kb.remove_all_hotkeys()          

    def Infos(self):
        self.dic_info = {
            'Atalho': [i.split(":")[0] for i in self.info.split('\n')[1:-1]],
            'Função': [i.split(":")[1] for i in self.info.split('\n')[1:-1]]
        }
        a = ''
        for i in self.info.split('\n')[1:]:
            try:
                a += f'{i.split(":")[0]}:  {i.split(":")[1]}\n\n'
            except:
                pass
        self.arq_abrev = self.ler_json(self.abreviacoes)
        for i, j in self.arq_abrev.items():
            a += f'{i}: {j} \n\n'

            # print(i,j)

        self.tabelaInfo = ft.Text(a, width=800, selectable=True, size = 18)

        self.controls = [self.tabelaInfo,ft.Row([self.abreviacao, self.Editar])]

    def Add_nova_abreviacao_lista(self, texto):
        self.saidad.visible = True
        self.saidad.controls.append(ft.Text(texto, selectable=True))
        self.update()
    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}
    def Save_abreviation(self, e,nome_json):
        abrev = self.abrev.value
        subst = self.subs.value
        if abrev != '' and subst != '':
            # print(f'{abrev} >> {subst}')
            kb.add_abbreviation(abrev, subst)
            self.arq_abrev = self.ler_json(nome_json)
            self.arq_abrev[abrev] = subst
            self.escrever_json(self.arq_abrev, nome_json)
            self.a.print_in_dialog(f'Nova abreviação adicionada ({abrev} >> {subst})')
            # self.Add_nova_abreviacao_lista(f'{abrev}: "{subst}"')

            # self.Exibir_na_tabela_de_saida(abrev, subst)

            self.tabelaInfo.value += f'{abrev}: {subst}\n'
            self.update()

    def CriarAbreviacao(self, e):
        lin1 = ft.Row(alignment='center')
        col1 = ft.Column(tight=True)
        self.abrev = TextField(label='abrev', border_width=1, expand=True)
        self.subs = TextField(label='subs', border_width=1, expand=True)
        lin1.controls.append(self.abrev)
        lin1.controls.append(self.subs)
        col1.controls.append(lin1)
        # self.saida_dialog.value = ''
        # col1.controls.append(self.saida_dialog)
        def sv(e):
            self.Save_abreviation(e, self.abreviacoes)
        # salvar = ft.ElevatedButton('Salvar',on_click=sv)
        # fechar =  ft.ElevatedButton('Fechar',on_click=self.Sair)

        # col1.controls.append(ft.Row([salvar, fechar], alignment='center'))
        # self.popoupM('Criar Atalho', col1)
        self.a = Poupup(title='Criar Atalho', funcao=sv, page = self.page, content = [col1])



    def Editar_atalhos(self,e):
        # self.controls = [self.tabelaInfo,self.abreviacao]
        class Edite_abrev(ft.ResponsiveRow):
            def __init__(self,  abrev = None, subs= None,func = None, num = None):
                # self.page = page
                super().__init__()
                self.func = func
                self.num = num
                def colun(x=1):
                    return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}
       
                self.abrev = TextField(value = abrev, label='abrev', border_width=1,  col = colun(2), dense=True, content_padding=8,multiline = True)
                self.subs = TextField(value = subs, label='subs', border_width=1,  col = colun(8), dense=True, content_padding=8,multiline = True)
                self.savar = ft.IconButton(ft.icons.SAVE, col = colun(1), data = ['save',0], on_click=self.Delete1)
                self.delete = ft.IconButton(ft.icons.AUTO_DELETE, col = colun(1), data = ['delete', self.num], on_click=self.Save1)
                self.controls = [self.abrev, self.subs,self.savar,self.delete]

            def Delete1(self, e):
                self.func(e)

            def Save1(self, e):
                self.func(e)
        self.arq_abrev = self.ler_json(self.abreviacoes)

        def Func(e):
            num = e.control.data[1]
            match e.control.data[0]:
                case 'delete':
                    def de(e):
                        abrev = self.controls[num].abrev.value
                        del self.arq_abrev[abrev]
                        del self.controls[num]
                        self.page.update()

                    c = Poupup('Confimar Exclusão?', de, self.page )

                case 'save':
                    abrev = self.controls[num].abrev.value
                    subs = self.controls[num].subs.value
                    self.arq_abrev[abrev] = subs
                    self.escrever_json(self.arq_abrev, self.abreviacoes)
                    Poupup('Salvo!', page = self.page)


               

        l = []
        num = 0
        for i, j in self.arq_abrev.items():
            l.append(Edite_abrev(i, j, Func, num))
            num+=1

        def sav2(e):
            d = {}
            a = ''
            for i in self.controls[:-1]:
                d[i.abrev.value] = i.subs.value
                a += f'{i.abrev.value}: {i.subs.value} \n\n'

            self.arq_abrev = d

                  

            self.tabelaInfo = ft.Text(a, width=800, selectable=True, size = 18)            
            self.escrever_json(self.arq_abrev, self.abreviacoes)
            self.controls = [self.tabelaInfo,ft.Row([self.abreviacao, self.Editar])]
            self.page.update()
        def sair(e):
            self.controls = [self.tabelaInfo,ft.Row([self.abreviacao, self.Editar])]
            self.page.update()            


        self.controls = l+[ft.Row([ft.ElevatedButton('Salvar', on_click=sav2),ft.ElevatedButton('Sair', on_click=sair)])]
        self.page.update()


    def Clic(self):
        # Obtém o estado atual do Caps Lock
        caps_lock_state = kb.is_pressed('caps lock')

        # Inverte o estado do Caps Lock
        kb.press_and_release('caps lock')

        # Restaura o estado anterior do Caps Lock
        if caps_lock_state:
            kb.press('caps lock')
        else:
            kb.release('caps lock')

        # Clique do mouse (pode ser ajustado conforme necessário)
        click()

class Saida2(ft.Column):
    def __init__(self, height=150, page = None):
        super().__init__()
        self.page = page
        self._height = height
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=self._height,  ),bgcolor='white,0.08' ))
    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        try:
            self.page.update()
        except:
            pass

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = height
        try:
            self.controls[0].content.height = self._height
            # print(self.controls[0])
            self.page.update()
        except:
            pass


class Saida:
    def __init__(self,  page = None):
        self.page = page
        self.snac = ft.SnackBar(
                    content = ft.Text('', selectable=True, color=ft.colors.BROWN_100),
                    open=True,
                    bgcolor=ft.colors.GREY_900,
                )
 
    
    def pprint(self, *texto):
        for i in list(texto):
            self.snac.content.value = f'{i}'
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass


class Poupup:
    def __init__(self, 
                 title = None, 
                 funcao = None,
                 page = None,
                 texto =None,
                 nomes_botoes = ['Sim', 'Não'],
                content = None
                 ):
        super().__init__()
        self.page = page
        self.title = title
        self._content = content
        self._funcao = funcao
        self._texto = texto
        self.dialogo1 = ft.AlertDialog(
            modal=False,
            open = True,
            title=ft.Row([ft.Text(self.title, weight='BOLD')],alignment='center'),
            shadow_color = ft.colors.TRANSPARENT,
            content_padding = ft.Padding(15,0,15,0),
            actions_padding = ft.Padding(0,10,0,0),
            title_padding = ft.Padding(4,0,4,0),
            
            bgcolor=ft.colors.GREY_900,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            alignment =ft.alignment.top_center,
        )
        if self._content != None:
            if isinstance(self._content, list):
                self.dialogo1.content = ft.Column([ft.Text(self._texto)], tight=True)
                self.dialogo1.content.controls += [i for i in self._content]

            else:
                self.dialogo1.content = ft.Column([ft.Text(self._texto)], tight=True)
                self.dialogo1.content.controls += [self._content]  
        


        
        if self._funcao != None:
            self.dialogo1.modal=True

            self.dialogo1.actions = [
                ft.Row([
                    ft.Container(
                        bgcolor = ft.colors.with_opacity(1, ft.colors.GREY_500),
                        border_radius = ft.BorderRadius(0,0,20,0),
                        on_click=self.yes_click,
                        padding= ft.Padding(0,10,0,10),
                        content = ft.Text(
                            nomes_botoes[0], 
                            weight = "BOLD", 
                            text_align='center',
                            size = 15,
                             color=ft.colors.PRIMARY,
                        ),
                        expand=True,
                    ),
                    ft.Container(
                        bgcolor = ft.colors.with_opacity(1, ft.colors.RED),
                        border_radius = ft.BorderRadius(0,0,0,20),
                        on_click=self.no_click,
                        padding= ft.Padding(0,10,0,10),
                        content = ft.Text(
                            nomes_botoes[1],
                              weight = "BOLD", 
                              text_align='center',
                              size = 15,
                              color=ft.colors.PRIMARY,
                            ),
                        expand=True,
                    ),
                                     
                ],
                spacing = 0,
                expand= True)
        
            ]

        self.page.overlay.append(self.dialogo1)
        self.page.update()

    @property
    def content(self):
        return self._content
    @content.setter
    def content(self, valor):
        self._content = valor
        if self._content != None and isinstance(self._content, list):
            self.dialogo1.content = ft.Column([ft.Text(self._texto)])
            self.dialogo1.content.controls += [i for i in self._content]
        elif isinstance(self._content, str) | isinstance(self._content, int):
            self.dialogo1.content.controls[0].value = self._texto
        
        self.dialogo1.update() 



    @property
    def texto(self):
        return self._texto
    @texto.setter
    def texto(self, valor):
        self._texto = valor
        if isinstance(self._content, str) | isinstance(self._content, int):
            self.dialogo1.content.controls[0].value = self._texto        
            self.dialogo1.update() 
        

        

    @property
    def funcao(self):
        return self._funcao
    @funcao.setter
    def funcao(self, valor):
        self._funcao = valor
        if self._funcao != None:
            self.dialogo1.modal=True
            self.dialogo1.actions = [
                ft.CupertinoDialogAction(
                'Sim',
                text_style=ft.TextStyle(italic=True),
                is_destructive_action=True,
                on_click=self.yes_click
            ),
                ft.CupertinoDialogAction(text='Não', is_default_action=False, on_click=self.no_click),

            ]
        self.dialogo1.update() 





    def yes_click(self,e):
        if self._funcao != None:
            self._funcao(e)
        sleep(0.5)
        self.dialogo1.open = False
        self.page.update()


    def no_click(self,e):
        self.dialogo1.open = False
        self.page.update()
    

    def print_in_dialog(self, texto):
        # self.saida_dialog.value = texto
        # self.dialogo1.Content.update()
        self.dialogo1.content.controls[0].value = texto
        self.dialogo1.update() 
    


    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'w') as f2:
            json.dump(nomedodicionario, f2, indent=4)

    def Ler_json(self, nomedoarquivo):  # retorna um dicionário
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'r') as f2:
            try:
                a = json.load(f2)
                return a
            except json.JSONDecodeError as e:
                print(f'Erro ao decodificar JSON: {e}')
                return {}

class Content_dialog(ft.Column):
    def __init__(self, nome_do_json,page):
        super().__init__()
        self.page = page
        self.nome_do_json = nome_do_json
        self.tecla = None
        self.page.on_keyboard_event = self.Teclas
        
        self.dic = self.Ler_json(nome_do_json,
                                 default={
                                        "loc_digitar_mensagen": [
                                            1871,
                                            1003
                                        ],
                                        "loc_cruz": [
                                            1731,
                                            998
                                        ],
                                        "loc_enquet": [
                                            1783,
                                            824
                                        ],
                                        "loc_documento": [
                                            1780,
                                            708
                                        ],
                                        "loc_pesquisar_contato": [
                                            1430,
                                            198
                                        ],
                                        "pasta_mandados": "D:\\baixados\\tjse\\mandados\\2014",
                                        "nome_do_oficial": "Lep",
                                        "matricula": "16668"
                                    }                
                                             
                                             )
        self.horizontal_alignment='center'
        self.tight=True
        self.controls = [ft.Text()]
        self.pasta = SaveSelectFile2('path', 'pasta dos mandados')
        self.pasta.value = self.dic['pasta_mandados']
        self.nome_do_oficial = ft.TextField(label='Nome do Oficial')
        self.nome_do_oficial.value = self.dic['nome_do_oficial']
        self.matricula = ft.TextField(label='Matrícula')
        self.matricula.value = self.dic['matricula']
        for i in self.dic.keys():
            if i == 'pasta_mandados':
                self.controls.append(self.pasta)
            elif i == 'nome_do_oficial':
                self.controls.append(self.nome_do_oficial)     
            elif i == 'matricula':
                self.controls.append(self.matricula)                             
            else:  
                self.controls.append(ft.Row([ft.Text(i), ft.OutlinedButton(
                'config', on_click=self.Config_pontos_tela, data=i)]))


    def print_in_dialog(self, texto):
        self.controls[0].value = texto
        self.update()

    def Config_pontos_tela(self, e):
        ponto = e.control.data
        self.print_in_dialog(
            f'leve o mouse até "{ponto}" e pressione "enter".')
        while self.tecla != 'enter':
            sleep(0.3)
        self.tecla = None
        self.print_in_dialog(f'Ponto capturado')

        self.dic[ponto] = position() 



    def Teclas(self, e: ft.KeyboardEvent):
        match e.key:
            case 'Enter':
                self.tecla = 'enter'
            case 'Escape':
                self.tecla = 'esc'
        self.page.update()
        

    def Savar_pontos(self, e):
        if self.pasta.value not in ['', None]:
            self.dic['pasta_mandados'] = self.pasta.value 
        if self.nome_do_oficial.value not in ['', None]: 
            self.dic['nome_do_oficial'] = self.nome_do_oficial.value 
        if self.matricula.value not in ['', None]:
            self.dic['matricula'] = self.matricula.value 

        self.Escrever_json(self.dic, self.nome_do_json)
        self.print_in_dialog('Pontos salvos com sucesso')


    def Escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def Ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}

class Content_dialog2(ft.Column):
    def __init__(self, json,nomejson, page):
        super().__init__()
        self.page = page
        self.json = json
        self.nomejson = nomejson
        self.tecla = None
        # self.width = 400
        self.page.on_keyboard_event = self.Teclas        
        self.dic = self.json
        self.horizontal_alignment='center'
        # self.tight=True
        self.spacing = 20
        self.controls = [ft.Text()]
        self.pasta = SaveSelectFile2('path', 'pasta dos mandados')
        self.pasta.value = self.dic['pasta_mandados']
        # self.nome_do_oficial = ft.TextField(label='Nome do Oficial')
        # self.nome_do_oficial.value = self.dic['nome_do_oficial']
        # self.matricula = ft.TextField(label='Matrícula')
        # self.matricula.value = self.dic['matricula']
        self.dic_objetos = {}
        self.campo = ft.TextField()
        # for i in self.dic.keys():
        #     if i == 'pasta_mandados':
        #         self.controls.append(self.pasta)
        #     elif i == 'nome_do_oficial':
        #         self.controls.append(self.nome_do_oficial)     
        #     elif i == 'matricula':
        #         self.controls.append(self.matricula)                             
        #     elif i in ["loc_digitar_mensagen", "loc_cruz", "loc_enquet", "loc_documento", "loc_pesquisar_contato"]:  
        #         self.controls.append(ft.Row([ft.Text(i), ft.OutlinedButton(
        #         'config', on_click=self.Config_pontos_tela, data=i)]))
        #     else:
        #         self.campo.label=i
        #         self.campo.value=self.dic[i]
        #         print(i,self.dic[i])
        #         self.controls.append(self.campo)  


        for i in self.dic.keys():    
            if i in ["loc_digitar_mensagen", "loc_cruz", "loc_enquet", "loc_documento", "loc_pesquisar_contato"]:
                self.dic_objetos[i] = ft.Row([ft.Text(i), ft.OutlinedButton('config', on_click=self.Config_pontos_tela, data=i)])
            else:
                self.dic_objetos[i] = ft.TextField(label = i, value = self.dic[i] , content_padding=12, dense=True, width=400, fill_color='white,0.3')

            self.controls.append(self.dic_objetos[i]) 

    def print_in_dialog(self, texto):
        self.controls[0].value = texto
        self.update()

    def Config_pontos_tela(self, e):
        ponto = e.control.data
        self.print_in_dialog(
            f'leve o mouse até "{ponto}" e pressione "enter".')
        while self.tecla != 'enter':
            sleep(0.3)
        self.tecla = None
        self.print_in_dialog(f'Ponto capturado')

        self.dic[ponto] = position() 



    def Teclas(self, e: ft.KeyboardEvent):
        match e.key:
            case 'Enter':
                self.tecla = 'enter'
            case 'Escape':
                self.tecla = 'esc'
        try:
            self.page.update()
        except:
            pass
        

    def Savar_pontos(self, e):
        # if self.pasta.value not in ['', None]:
        #     self.dic['pasta_mandados'] = self.pasta.value 
        # if self.nome_do_oficial.value not in ['', None]: 
        #     self.dic['nome_do_oficial'] = self.nome_do_oficial.value 
        # if self.matricula.value not in ['', None]:
        #     self.dic['matricula'] = self.matricula.value 
        for i in self.dic_objetos.keys():
            if i not in ["loc_digitar_mensagen", "loc_cruz", "loc_enquet", "loc_documento", "loc_pesquisar_contato"]:                
                if self.dic_objetos[i].value not in ['', None]:
                    self.dic[i] = self.dic_objetos[i].value 

        self.Escrever_json(self.dic, self.nomejson)
        self.print_in_dialog('Pontos salvos com sucesso')


    def Escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def Ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}


class SaveSelectFile2(ft.Row):
    def __init__(self, tipo, nome = None):
        '''
        tipo  == path: seleciona uma pasta (retorna o caminho completo da pasta selecionada)
        tipo  == file: seleciona um arquivo (retorna o caminho completo do arquivo selecionado)
        tipo  == save: sala um arquivo (retorna o caminho completo do arquivo, junto com seu nome)
        
        '''
        super().__init__()
        self.nome = nome
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.tamanho_texto = 500
        self.selected_files = ft.Text(width=self.tamanho_texto, selectable=True, max_lines = 1)
        self._value = self.selected_files.value
        self.tipo = tipo
        self.visible = True

        async def Selecionar_arquivo(_):
            await self.pick_files_dialog.pick_files_async(allow_multiple=True)

        async def Selecionar_pasta(_):
            await self.pick_files_dialog.get_directory_path_async(dialog_title = 'askdjahs', initial_directory = r'D:\baixados\programas_python\TabelaMandado\baixaryoutube\baixar_do_youtube\build\web')

        async def Save1(_):
            await self.pick_files_dialog.save_file()            



        if tipo == 'file':
            if self.nome == None:
                self.nome = 'Selecione o arquivo'            
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=Selecionar_arquivo,
                ),
                self.selected_files,
            ]
        elif tipo == 'path':
            if self.nome == None:
                self.nome = 'Selecione a pasta'
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.FOLDER,
                    on_click=Selecionar_pasta,
                ),
                self.selected_files,
            ]   
        elif tipo == 'save':
            if self.nome == None:
                self.nome = 'Digite o nome do arquivo'            
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.SAVE,
                    on_click=Save1,
                ),
                self.selected_files,

            ]                      

    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        if self.tipo == 'file':
            self.selected_files.value = (
                ",".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
            )
        elif self.tipo == 'path':
            self.selected_files.value = e.path if e.path else "Cancelled!"

        elif self.tipo == 'save':
            self.selected_files.value = e.path if e.path else "Cancelled!"            
            

        await self.selected_files.update_async()
        self._value = self.selected_files.value


    # happens when example is added to the page (when user chooses the FilePicker control from the grid)
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()

    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    def will_unmount(self):
        self.page.overlay.remove(self.pick_files_dialog)
        self.page.update()

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, valor):
        self._value = valor
        self.selected_files.value = valor
        # self.selected_files.update()

class PopupMenu(ft.UserControl):
    def __init__(self, 
                 nome_ou_icone = None, 
                 lista_de_controles = None,
                 tooltip = None,
                 col = None,
            ):
        super().__init__()
        self.nome_ou_icone = nome_ou_icone
        self.tooltip = tooltip
        self._colu = col
        self.p = ft.PopupMenuButton(tooltip = self.tooltip, col = self._colu)
        self.lista_de_controles = lista_de_controles
        self._Add_itens()

    @property
    def coluna(self):
        return self._colu
    
    @coluna.setter
    def coluna(self, valor):
        self._colu = valor
        # self.p.col = valor
        

    def _Add_itens(self):
        if isinstance(self.lista_de_controles, list) and len(self.lista_de_controles) > 0:
            self.p.items = [ft.PopupMenuItem(content = i) for i in self.lista_de_controles]
        else:
            print('Não há itens para adicionar')

    def Add_item(self, *controle):
        for i in list(controle):
            self.p.items.append(ft.PopupMenuItem(content = i,))
        # self.p.update()

    def build(self):
        if self.nome_ou_icone != None and (isinstance(self.nome_ou_icone, ft.Icon) or isinstance(self.nome_ou_icone, Text)):
            self.p.content = self.nome_ou_icone
        return self.p

class ItensPoup: #classe para criar controles para a classe PopupMenu2
    def __init__(self,
                 
        icon = None,
        text = None,
        on_click = None ,
        data = None,
        cor = None,
              
                 
        ):
        self.icon = icon
        self.quebra_linha(text, largura=30)
        self.on_click = on_click
        self.data = data
        self.cor = cor

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, texto):
        self.quebra_linha(texto, largura=30)

    def quebra_linha(self, texto, largura=36):
        palavras = texto.split()
        linhas = []
        linha_atual = ''
        
        for palavra in palavras:
            if len(linha_atual) + len(palavra) <= largura:
                linha_atual += palavra + ' '
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + ' '
        
        if linha_atual:
            linhas.append(linha_atual.strip())
        
        self._text  = '\n'.join(linhas)

class PopupMenu2(ft.UserControl):
    def __init__(self, 
                 nome_ou_icone = None, 
                 controles:ItensPoup = None, #[icone, nome, on_click, data]
                 tooltip = None,
                 col = None,
            ):
        super().__init__()
        self.nome_ou_icone = nome_ou_icone
        self.tooltip = tooltip
        self._colu = col
        self.p = ft.PopupMenuButton(tooltip = self.tooltip)
        self.lista_de_controles = controles
        self._Add_itens()

    @property
    def coluna(self):
        return self._colu
    
    @coluna.setter
    def coluna(self, valor):
        self._colu = valor
        # self.p.col = valor
        

    def _Add_itens(self):
        if isinstance(self.lista_de_controles, list) and len(self.lista_de_controles) > 0:
            self.p.items = [ft.PopupMenuItem(icon = i.icon, text = i.text, on_click = i.on_click, data = i.data) for i in self.lista_de_controles]
        else:
            print('Não há itens para adicionar')

    def Add_item(self, *controle):
        
        for i in list(controle):
            if isinstance(i,ItensPoup ):
            # try:
            #     icon = i[0] 
            # except:
            #     icon = None
            # try:
            #     text = i[1] 
            # except:
            #     text = None
            # try:
            #     on_click = i[2] 
            # except:
            #     on_click = None
            # try:
            #     data = i[3]
            # except:  
            #     data = None
            
                self.p.items.append(ft.PopupMenuItem(icon = i.icon, text = i.text, on_click = i.on_click, data = i.data))
        # self.p.update()

    def Add_item_control(self, *controle):        
        for i in list(controle):
            if isinstance(i,ItensPoup ):
                icone = ft.Icon(i.icon, color = i.cor)
                texto = ft.Text(i.text,color = i.cor)
                if i.icon == None:
                    icone.visible = False
                if i.text == None:
                    texto.visible = False
                conteudo = ft.Row([icone,texto])
                if i.text == None and i.icon == None:
                    conteudo = None
                self.p.items.append(ft.PopupMenuItem(content = conteudo, on_click=i.on_click))


    def Add_item_geral(self, *controle):        
        for i in list(controle):
            if isinstance(i,ft.PopupMenuItem):
                self.p.items.append(i)


    def build(self):
        if self.nome_ou_icone != None and (isinstance(self.nome_ou_icone, ft.Icon) or isinstance(self.nome_ou_icone, Text)):
            self.p.content = self.nome_ou_icone
        return self.p
# class Tabs_new(ft.UserControl):
#     def __init__(self,
#         data = None,
#         on_change = None,
#         tabs:list['nome',Control] = None, # type: ignore
#         width=200,
#         height=200,
        
                 
#     ):
#         super().__init__()
#         self.data = data
#         self.on_change = on_change
#         self.w = width
#         self.h = height
#         self.tabs = tabs
#         self.Construir_tabs()
#         self.t = ft.Tabs(
#             selected_index=0,
#             animation_duration=0,
#             # divider_color  = 'blue',
#             tabs=self.tabs_construidas,
#             width=self.w,
#             height=self.h,
#             data = self.data,
#             on_change=self.Func,
#             # expand=1,
            
#             )
#         # self.height2 = None
#         # self.width = None

#     def Func(self,e):
#         if self.on_change is not None:  
#             return self.on_change(self,e)
        
#     def Construir_tabs(self):
#         self.tabs_construidas =  [ft.Tab(text=i[0],  content = i[1]) for i in self.tabs]

#     def Add_tab(self, *tabs:['nome',Control]): # type: ignore
#         self.tabs_construidas +=  [ft.Tab(text=i[0],  content = i[1]) for i in tabs]
#         # self.t.update()

#     @property
#     def get_height(self):
#         return self.h 
#     @get_height.setter
#     def set_height(self, valor):
#         self.h = valor
#         self.t.height = valor
#         # self.t.update()

#     @property
#     def get_width(self):
#         return self.w 
#     @get_width.setter
#     def set_width(self, valor):
#         self.w = valor
#         self.t.width = valor
#         # self.t.update()


#     def build(self):
#         return self.t
# class Dialogo(ft.UserControl):
#     def __init__(self,

#                  title: str = 'título da janela',
#                  content: Control | None = None,
#                  on_dismiss: None = None,
#                  salvar=None,
#                  nome_json=None
#                  ):
#         super().__init__()
#         # self.page = page
#         self.titulo = title
#         self._content = content
#         self.on_dismiss = on_dismiss
#         self.salvar = salvar
#         self.nome_json = nome_json
#         self.dlg_modal = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(self.titulo),
#             content=self._content,
#             actions=[
#                 ft.TextButton("Salvar", on_click=self.Salvar),
#                 ft.TextButton("Sair", on_click=self.close_dlg),
#                 # ft.TextButton("No", on_click=self.close_dlg),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             on_dismiss=self.on_dismiss,
#         )

#     def build(self):
#         return self.dlg_modal

#     def open_dlg_modal(self):
#         # self.page.dialog = self.dlg_modal
#         self.dlg_modal.open = True
#         self.update()

#     def att(self):
#         # self._content = ft.Text('casdada')
#         self.dlg_modal.content = ft.Text('casdada')
#         self.update()

#     def close_dlg(self, e):
#         self.dlg_modal.open = False
#         self.update()

#     def Salvar(self, e):
#         return self.salvar(e, self.nome_json)

#     @property
#     def Content(self):
#         return self._content

#     @Content.setter
#     def Content(self, valor):
#         self._content = valor
#         self.dlg_modal.content = self._content
#         self.update()

#     @property
#     def Titulo(self):
#         return self.titulo

#     @Titulo.setter
#     def Titulo(self, valor):
#         self.titulo = valor
#         self.dlg_modal.title = ft.Text(self.titulo)
#         self.update()
# class ShowDF(ft.UserControl):
#     def __init__(self,
#                  df#DataFrame ou dicionário
#                  ):
#         super().__init__()
#         self.df = df if type(df) != dict else DataFrame(df)
#         self.d1 = ft.DataTable(border = ft.border.all(1,'white,0.9'),
#                             heading_row_color = 'white,0.5',
#                             heading_row_height = 80,
#                             column_spacing = 15,
#                             # heading_row_color=ft.colors.BLACK12,
#                             vertical_lines = ft.border.all(20,'white'),
#                             horizontal_margin = 0,
#                             data_row_max_height = 70,
#                             # data_row_min_height = 50,
#                             divider_thickness = 0,
#                             show_checkbox_column = True,
#                             sort_column_index = 4,
#                             sort_ascending = True,
#                             # data_row_color={"hovered": "0x30FF0000"},
#                             )
#         self.textsize = 15
#         self.Colunas_tabela()
#         self.Linhas_tabela()

#     def Colunas_tabela(self):
#         self.d1.columns = [ft.DataColumn(ft.Row([ft.Text(width=10),ft.Text(i,selectable = True,theme_style=TextThemeStyle.TITLE_MEDIUM)],alignment='center')) for i in list(self.df.columns)]
        
    
#     def Linhas_tabela(self):
#         linhas = []
#         df_lista = self.df.values.tolist()
#         for l,i in enumerate(df_lista):
#             cell = [ ft.DataCell(ft.Row([ft.Text(width=10),ft.Text(j,text_align='center',selectable = True, size = self.textsize)],alignment='left',spacing = 3,)) for j in i]
#             cor  = 'black' if l % 2 == 0 else 'white,0.01'
#             linhas.append(ft.DataRow(cells = cell, color = cor))
#         self.d1.rows = linhas
            
#     def build(self):
#         return self.d1
# class TabelaMandadosAcoes(ShowDF):
#     def __init__(self, df, funcao):
#         self.larguras()
#         super().__init__(df)
#         self.funcao = funcao

#     def larguras(self):
#         self.largura = {
#             'Nº do Processo:':80, 
#             'Nº do mandado:':80, 
#             'Destinatario do mandado:':100,
#             'Endereco':650, 
#             'ação':60, 
#             'Tipo do mandado:':80, 
#             'Audiência':90,
#             'Final de prazo':90, 
#             'telefone':70
#         }
   
#     def Colunas_tabela(self):
#         for j,i in enumerate(list(self.df.columns)):
#             match i:
#                 case 'ação':
#                     largura = 85 
#                 case _:
#                     largura = 90
#             linha = ft.Row([
#                 ft.Text(i, text_align='center', selectable=True, width=self.largura[i],color = 'black',weight = 'bold',
#                      theme_style=TextThemeStyle.TITLE_MEDIUM, col={'xs': 12}),
#                 # ft.Row([
#                     ft.IconButton(ft.icons.ARROW_DROP_UP_SHARP, width=25,on_click = self.ordem,data = [i,True],
#                                icon_color='black,0.8', col={'xs': 6}),
#                     ft.IconButton(ft.icons.ARROW_DROP_DOWN_SHARP, width=25,on_click = self.ordem,data = [i,False],
#                                icon_color='black,0.8', col={'xs': 6}),
#                     ft.Text(width=10)
#                 # ], alignment='left', tight=True,)
#                 # ft.Text(width=15)
#             ],
#                 # horizontal_alignment='center',
#                 # alignment="spaceEvenly",
#                 tight=True,
#                 spacing=0,
#                 height=200,
#                 run_spacing=0)
#             self.d1.columns.append(ft.DataColumn(linha, data=i))

#         # self.d1.columns = [ft.DataColumn() for i in list(self.df.columns)] + [ft.DataColumn(ft.Text('Enviar'))
#         self.d1.columns.append(ft.DataColumn(ft.Text(' Enviar ',color = 'black',), data='Enviar'))
#         self.d1.columns.append(ft.DataColumn(ft.Text(' PDF ',color = 'black',), data='PDF'))
#         self.d1.columns.append(ft.DataColumn(ft.Text(' Add ',color = 'black',), data='Add'))
#         self.d1.columns.append(ft.DataColumn(ft.Text(' Mand.\ndireto ',color = 'black',), data='Mand.D'))

#     def Linhas_tabela(self):
#         linhas = []
#         df_lista = self.df.values.tolist()
#         indx = list(self.df.index)

#         nomes_colunas = ['Nº do Processo:', 'Nº do mandado:', 'Destinatario do mandado:',
#                          'Endereco', 'ação', 'Tipo do mandado:', 'Audiência',
#                          'Final de prazo', 'telefone']
        


#         acao1 = ['aguardar', 'cancelar', 'consultar', 'devolver', 'email', 'enviado', 'imp_', 'impresso', 'ligar',
#                  'Não encontrei', 'transferido', 'Transferir', 'voltar', 'zap']
        
#         tipo1 = ['Afastamento',	'Avaliação',	'Busca',	'Citação',	'Citação e Intimação',	'Condução',	'Contramandado',
#                  'Entrega',	'Imissão',	'Intimação',	'Intimação para Audiência',	'Notificação',	'Ofício',	'Penhora',	'Prisão',	'Reintegração']
#         tipo1 = list(map(str.upper, tipo1))


#         for l, i in enumerate(df_lista):
#             cell = []

#             for k, j, num_col in zip(list(self.df.columns), i, range(200)):

#                 if k in ['Destinatario do mandado:']:
#                     cell.append(
#                         ft.DataCell(
#                                     ft.Row([
#                                         ft.Text(
#                                                 j, selectable=True,
#                                                 size=15,text_align = TextAlign.CENTER,
#                                                 weight = FontWeight.BOLD,
#                                                 width=self.largura[k]+100
#                                             ),
#                                         ft.IconButton(icon = ft.icons.SEARCH, scale = 1, icon_size = 13, data = [indx[l],'pesquisar',j], on_click=self.Func, tooltip = 'Pesquisar contato no zap')
#                                     ], spacing=0, tight=True, run_spacing = 0),
#                                     data = [indx[l],'copiado',j],
#                                     on_double_tap = self.Func
#                                 )
                                
#                         )
               
#                 elif k in ['Endereco']:
#                     cell.append(ft.DataCell(ft.Text(j, selectable=True, size=12,text_align = TextAlign.START,
#                                               width=self.largura[k]+100),
#                                                 data = [indx[l],'copiado',j],
#                                                 on_double_tap = self.Func                                              
#                                               ))
                              
               
#                 elif k == 'ação':
#                     match j:
#                         case 'zap':
#                             cor = 'green' 
#                         case 'enviado':
#                             cor = 'yellow,0.3'                         
#                         case 'aguardar':
#                             cor = 'blue,0.8'                        
#                         case 'impresso':
#                             cor = 'white,0.1'     
#                         case 'devolver':
#                             cor = 'red'
#                         case 'imp_':
#                             cor = 'blue'
#                         case 'Transferir':
#                             cor = 'white,0.5'                                                                                                                   
#                         case _:
#                             cor = 'black'                    
#                     cell.append(ft.DataCell(ft.Container(ft.Row([Drop_new(acao1, value=j,alinhamento = ft.Alignment(-1, 0),
#                                                        width_person=self.largura[k]+50,
#                                                        on_change=self.Func2,
#                                                        data=[indx[l],'acao2',[l,num_col]])],
#                                              alignment='left'),bgcolor=cor)))
                
                
#                 elif k == 'Tipo do mandado:':
#                     v = list(map(str.upper, [j])) if j not in [None,'', '--'] else ['--']
#                     tipo2 = tipo1[:]
#                     if v[0] not in tipo1:
#                         tipo2.append(v[0])
#                     cell.append(ft.DataCell(ft.Row([Drop_new(tipo2, value=v[0], width_person=self.largura[k]+50,alinhamento = ft.Alignment(-1, 0),
#                                                        on_change=self.Func2, data=[indx[l],'tipo2',[l,num_col]])], alignment='center')))
               
               
#                 elif k == 'telefone':
#                     cell.append(ft.DataCell(ft.Row([ft.Text(j, selectable=True, 
#                                               )],alignment='center', expand=1, width=120),
#                                                 data = [indx[l],'copiado',j],
#                                                 on_double_tap = self.Func    
#                                               ))
              
#                 elif k in ['Nº do Processo:']:
#                     cell.append(ft.DataCell(ft.Row([ft.Text(j, selectable=True, text_align='center',
#                                               width=100)],alignment='center'),
#                                             data = [indx[l],'copiado',j],
#                                             on_double_tap = self.Func                                                
#                                               ))

#                 elif k in ['Nº do mandado:']:
#                     cell.append(ft.DataCell(ft.Row([ft.Text(j, selectable=True, text_align='center',
#                                               width=100),
#                                         ft.IconButton(icon = ft.icons.PICTURE_AS_PDF, scale = 1, icon_size = 13, data = [indx[l],'ver_pdf',j], on_click=self.Func, tooltip = 'Visualizar PDF')

                                              
#                                               ],alignment='center'),
#                                             data = [indx[l],'copiado',j],
#                                             on_double_tap = self.Func                                                
#                                               ))                    
                




#                 elif k == 'Audiência':
#                     try:
#                         data_audiencia =  findall(r'(\d{2}/\d{2}/\d{4})', j)[0]
                    

#                         current_time = datetime.now()
#                         cor2  = None
#                         # Função para converter string "dd/mm/yy" para datetime
#                         def converter_para_datetime(data_string):
#                             return datetime.strptime(data_string, '%d/%m/%Y')
#                         if len(data_audiencia) > 5:
#                             try:
#                                 data_convertida = converter_para_datetime(data_audiencia)
#                             except:
#                                 print(j[:-9])
#                                 data_convertida = converter_para_datetime(j[:-9])

#                             diferenca = data_convertida - current_time
                        

#                             if diferenca.days < 8:
#                                 cor2  = 'red,0.5'
#                             elif diferenca.days < 16:
#                                 cor2  = 'yellow,0.3'
#                             else:
#                                 cor2  = None
#                     except:
#                         cor2  = None


#                     cell.append(ft.DataCell(ft.Container(ft.Row([ft.Text(j, text_align='center', selectable=True,max_lines = 1, no_wrap = True)],alignment='center'),bgcolor=cor2),
#                                             data = [indx[l],'copiado',j],
#                                             on_double_tap = self.Func                                         
#                                          ))
                
#                 elif k == 'Final de prazo':
#                     try:
#                         prazo = findall(r'(\d{2}/\d{2}/\d{4})', j)[0]
#                         current_time = datetime.now()
#                         cor2  = None
#                         # Função para converter string "dd/mm/yy" para datetime
#                         def converter_para_datetime(data_string):
#                             return datetime.strptime(data_string, '%d/%m/%Y')
#                         if len(prazo) > 5:
#                             prazo_convertido = converter_para_datetime(prazo)

#                             diferenca = prazo_convertido - current_time

#                             if diferenca.days < 8:
#                                 cor2  = 'red,0.5'
#                             elif diferenca.days < 16:
#                                 cor2  = 'yellow,0.3'
#                             else:
#                                 cor2  = None
#                     except:
#                         cor2  = None


#                     cell.append(ft.DataCell(ft.Container(ft.Row([ft.Text(j, text_align='center', selectable=True,max_lines = 1, no_wrap = True)],alignment='center'),bgcolor=cor2)))             
               
#                 else:
#                     lagura = larg[k] if k in range(len(larg)) else 90
#                     cell.append(ft.DataCell(ft.Row([ft.Text(j, text_align='center', selectable=True,
#                                               )],alignment='center')))

#             cell.append(ft.DataCell(ft.Row([ft.IconButton(icon=ft.icons.SEND, 
#                 tooltip='Enviar Mandado', on_click=self.Func,
#                 data=[indx[l],'enviar'])])))
            
#             cell.append(ft.DataCell(ft.Row([ft.IconButton(icon=ft.icons.PICTURE_AS_PDF_OUTLINED,
#                 tooltip='Enviar PDF', 
#                 on_click=self.Func, data=[indx[l],'pdf',[l]])])))
            
#             cell.append(ft.DataCell(ft.Row([ft.IconButton(icon=ft.icons.PERM_CONTACT_CAL_ROUNDED,
#                 tooltip='Add Contato', 
#                 on_click=self.Func, data=[indx[l],'add'])])))     

#             cell.append(ft.DataCell(ft.Row([ft.IconButton(icon=ft.icons.CANCEL_SCHEDULE_SEND_OUTLINED,
#                 tooltip='Enviar Mandado direto \npara o contato \naberto no zap', 
#                 on_click=self.Func, data=[indx[l],'Mand.D',[l]])])))                    

#             cor = 'black' if l % 2 == 0 else 'white,0.05'
#             linhas.append(ft.DataRow(cells=cell, color=cor))
#         self.d1.rows = linhas

#     def FuncCopy(self, e):
#         nome = e.control.data
#         copy(nome)
#         self.funcao(e)

#     def Func(self, e):
#         encontrou = False

#         if e.control.data[1] in ['Mand.D','pdf']:
#             for j,i in enumerate(list(self.df.columns)):
#                 if i == 'ação':
#                     encontrou = True
#                     break
            
#             if encontrou:
#                 self.d1.rows[int(e.control.data[2][0])].cells[j].content.content.controls[0].getvalue = 'enviado'
#                 self.d1.rows[int(e.control.data[2][0])].cells[j].content.bgcolor = 'yellow,0.3'
#                 self.d1.update()




#         self.funcao(e)

#     def Func2(self, v, e):
#         # print('mudar cor')
#         match e.control.value:
#             case 'zap':
#                 cor = 'green' 
#             case 'enviado':
#                 cor = 'yellow,0.3'                         
#             case 'aguardar':
#                 cor = 'blue,0.8'                        
#             case 'impresso':
#                 cor = 'white,0.1'     
#             case 'devolver':
#                 cor = 'red'
#             case 'imp_':
#                 cor = 'blue'
#             case 'Transferir':
#                 cor = 'white,0.5'                                                                                                                   
#             case _:
#                 cor = 'black'        
#         # print(cor)
#         self.d1.rows[int(e.control.data[2][0])].cells[e.control.data[2][1]].content.bgcolor = cor
#         # print(self.d1.rows[int(e.control.data[2][0])].cells[e.control.data[2][1]].content.bgcolor)
#         self.d1.update()
#         self.funcao(e)

#     def duplo_clic(self, e):
#         print('duplo clic')


#     def ordem(self,e):
#         coluna, ascendente  = e.control.data

#         if coluna in ['Final de prazo', 'Audiência']:
#             try:
#                 self.df[coluna] = to_datetime(self.df[coluna], format = "%d/%m/%Y %H:%M:%S", dayfirst = True)
#             except:
#                 pass
#             self.df = self.df.sort_values(by=coluna,ascending = ascendente)
#             try:
#                 self.df[coluna] = self.df[coluna].dt.strftime("%d/%m/%Y %H:%M:%S")
#             except:
#                 pass         
#         else:
#             self.df = self.df.sort_values(by=coluna,ascending = ascendente)
#         self.Linhas_tabela()
#         self.d1.update()
# class TableCreate(ft.UserControl):
#     def __init__(self,borda: bool = False):
#         super().__init__()
#         self.borda = ft.border.all(1,'white,0.3') if borda else None
#         self.coluna = None
#         self.linha = None
#         self.d2 = ft.DataTable(border = self.borda, heading_row_color = 'white,0.1')

#     @property
#     def Coluna(self):
#         return self.coluna
    
#     @Coluna.setter
#     def Coluna(self,controle):
#         self.d2.columns.append(ft.DataColumn(controle))
#         # self.update()

#     @Coluna.setter
#     def Colunas(self,list_controles):
#         self.d2.columns = [ft.DataColumn(i) for i in list_controles]
#         # self.update()        
    
#     @property
#     def Linha(self):
#         return self.linha

#     @Linha.setter
#     def Linha(self,linha):
#         for i in enumerate(linha):
#             cell = [ ft.DataCell(j) for j in i]
#         self.d2.rows.append(ft.DataRow(cells = cell))
#         # self.update() 

#     @Linha.setter
#     def linhas(self,list_linhas):
#         linhas = []
#         for l,i in enumerate(list_linhas):
#             cell = [ ft.DataCell(j) for j in i]
#             cor  = 'black' if l % 2 == 0 else 'white,0.01'
#             linhas.append(ft.DataRow(cells = cell, color = cor))
#         self.d2.rows = linhas
#         # self.update()        

            
#     def build(self):
#         return self.d2

class ConfirmarSaida:
    def __init__(self,page, funcao = None):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.page.window.prevent_close = True 
   


    def window_event(self, e):
            if e.data == "close":
                self.page.dialog = self.confirm_dialog
                
                self.confirm_dialog.open = True
                self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()


class ConfirmarSaidaeResize:
    def __init__(self,page, funcao = None, exibir = True, width_min = None, height_min = None, onlyresize = False):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.width_min = width_min
        self.height_min = height_min
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.onlyresize = onlyresize
        if not onlyresize:
            self.page.window.prevent_close = True 

        self.page.on_resized = self.page_resize
        # self.page.window.on_event = self.page_resize
        self.nome = f'{self.page.title}_tamanho'
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados() 


    async def window_event(self, e):
        if e.data == 'resized' or e.data == 'moved':
            await self.page_resize(e)
        if e.data == "close" and not self.onlyresize:
            self.page.overlay.append(self.confirm_dialog)
            
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()



    async def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        valores = [self.page.window.width,self.page.window.height,self.page.window.top,self.page.window.left]
        if self.height_min:
            if valores[1]< self.height_min:
                valores[1] = self.height_min
        if self.width_min:
            if valores[0]< self.width_min:
                valores[0] = self.width_min      
        if valores[2] <0:
              valores[2] = 0   
        if valores[3] <0:
              valores[3] = 0                
        # with open('assets/tamanho.txt', 'w') as arq:
        #     arq.write(f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        await self.page.client_storage.set_async(self.nome, f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        

  

    def Ler_dados(self):
        try:
            # with open('assets/tamanho.txt', 'r') as arq:
            #     po = arq.readline()

            po = self.page.client_storage.get(self.nome)

            p1 = po.split(',')
            p = [int(float(i)) for i in p1]
            po = p[:4] 

            if self.width_min:
                if po[0]< self.width_min:
                    po[0] = self.width_min  
            if self.height_min:
                if po[1]< self.height_min:
                    po[1] = self.height_min 
            if po[2] <0:
                po[2] = 0   
            if po[3] <0:
                po[3] = 0                                   

            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po
            # print('acerto')
        except:
            # print('erro!')
            # with open('assets/tamanho.txt', 'w') as arq:
            #     arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = self.width_min,self.height_min,0,0



class Countdown(ft.UserControl):
    def __init__(self, minutos, texto = ''):
        super().__init__()
        # self.page = Page
        self.minutos = minutos
        self.segundos = 60*minutos
        self.texto = texto
        self.pause = False

    def did_mount(self):
        self.running = True
        if self.minutos != '':            
            Thread(target=self.update_timer, daemon=True).start()

        else:
            self.countdown.value = self.texto
            self.update()

    def will_unmount(self):
        self.running = False

    def update_timer(self):
        while self.segundos and self.running:
            h, mins = divmod(self.segundos, 60*60)
            mins, secs = divmod(mins, 60)
            h, mins, secs = int(h), int(mins), int(secs)
            if self.texto != '':
                self.countdown.value = "{:s} {:02d}:{:02d}:{:02d}".format(self.texto,h, mins, secs)
            else:
                self.countdown.value = "{:02d}:{:02d}:{:02d}".format(h, mins, secs)

            self.update()
            sleep(1)
            self.segundos -= 1
            while self.pause:
                sleep(0.3)
          

    def build(self):
        self.countdown = ft.Text()
        return self.countdown
'''
class Quadro(ft.UserControl):
    def __init__(self, 
                content = None,
                #  page = Page,
                 width = None, 
                 height = None,
                 expand = 0,
                 bgcolor = None,
                 border_color = 'blue',
                 
                 ):
        super().__init__()
        # self.page = page
        self.content = content
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.border_color = border_color
        self.expand = expand
        self.bgcolor = bgcolor
    
    def build(self):
        return ft.Container(
        content = self.content,
        border_radius=10,
        alignment=ft.Alignment(0,0),
        border= ft.border.all(0.2, color = self.border_color),
        width= self.width,
        height= self.height,
        expand = self.expand,
        bgcolor = self.bgcolor
        )
'''
class Contador(ft.Row):
    def __init__(self, 
                 segundos = 10,
                 cor = 'green',
                 size = 50,
                 page = None

    ):
        super().__init__()
        self.page = page
        self.segundos = segundos
        self.cor = cor
        self.size = size
        self.visible=False
        self.pause_contador = False
        self.tempo = ft.Text(color  = self.cor, size = self.size)
        self.controls = [self.tempo]

    def did_mount(self):
        self.Cont()


    @property
    def Pause(self):
        return self.pause_contador
    
    @Pause.setter
    def Pause(self, valor: bool):
        self.pause_contador = valor
        self.atualizar()

    def atualizar(self):
        if hasattr(self, 'page'):
            self.update()
        # except:
        #     pass
       






    def Cont(self):
        self.visible = True
        while self.segundos >= 0:
            horas2, minutos2, segundos2 = self.converter_segundos_para_horas_min_segundos(self.segundos)
            self.tempo.value = f"{horas2}:{minutos2}:{segundos2}"
            self.atualizar()
            self.segundos += -1
            sleep(1)
            while self.pause_contador:
                sleep(0.1)
        self.visible = False





    def converter_segundos_para_horas_min_segundos(self, segundos):
        def Algarismos(numero, qtd=2):
            numero = int(numero)
            return str(numero).zfill(qtd)
        horas = segundos // 3600  # 3600 segundos em uma hora
        horas = Algarismos(horas)
        segundos %= 3600
        minutos = segundos // 60  # 60 segundos em um minuto
        minutos = Algarismos(minutos)
        segundos %= 60
        segundos = Algarismos(segundos)
        # print(horas, minutos, segundos)
        return horas, minutos, segundos
    
class Quadro_assync(ft.UserControl):
    def __init__(self, 
                content = None,
                 tipo = 'r', #ou 'c'
                #  page = Page,
                 width = None, 
                 height = None,
                 expand = 1,
                 bgcolor = None,
                 border_color = 'white',
                 
                 ):
        super().__init__()
        # self._page = page
        self.tipo = tipo
        self.content = content #ft.Row(content) if self.tipo == 'r' else ft.Column(content)
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.border_color = border_color
        self.expand = expand
        self.bgcolor = bgcolor
    
    def build(self):
        return ft.Container(
        content = self.content,
        alignment=ft.Alignment(0,0),
        border = ft.border.all(1, color = self.border_color),
        width= self.width,
        height= self.height,
        expand = self.expand,
        bgcolor = self.bgcolor
        )
class Drop_new(ft.UserControl):
    def __init__(self, 
        opitions = [], 
        value = None,
        width_person = None,
        on_change = None,
        data = None,
        cor  = None,
        alinhamento = ft.Alignment(0, 0),
        label = None

                
                ):
        super().__init__()
        self.opitions  = opitions
        self.value = value
        self._width = 30 if opitions == [] else 80
        self.on_change = on_change
        self.data = data
        self.cor = cor
        self.alinhamento = alinhamento
        self._label = label

        if width_person != None:
            self._width = width_person         
 
        self._drop = ft.Dropdown(        
                alignment= self.alinhamento,
                options=[ft.dropdown.Option(i) for i in self.opitions],
                text_size = 15,
                border_width = 0,
                border=None,
                content_padding = 5,
                # border_color='white',
                expand=0,
                scale=1,
                autofocus = 0,
                value = self.value,
                width = self._width,
                # aspect_ratio = 1,
                height = 25,
                dense = True,
                text_style = TextStyle(weight = 'bold'),
                on_change=self.mudou,
                data  = self.data,
                bgcolor = self.cor,
                label = self._label,
                                                  
        ) 

    def build(self):  
        return self._drop
    
    def mudou(self, e):
        self.value = self._drop.value
        if self.on_change != None:
            self.enviar_change(e)
        self.update()

    def enviar_change(self,e):
        self.on_change(self, e)


    @property
    def getvalue(self):
        return self._drop.value
    @getvalue.setter
    def getvalue(self, valor):
        self._drop.options.append(ft.dropdown.Option(valor))
        self._drop.value = valor
        super().update()

class New_task2(ft.UserControl):
    def __init__(self,
        task_delete,
        nome='',
        duracao=3,
        inicio=70,
        fim=170,
        passo = 1,
        ):
        super().__init__()
        self.task_delete = task_delete
        self.nome_tarefa = TextField(hint_text = 'nome da tarefa', width = 200, capitalization = TextCapitalization.CHARACTERS, value = nome, height=30, border_width = 0,dense=True)
        self.duracao_tarefa = Drop_new([0.1,0.3,0.5]+[i for i in range(1,31)], duracao, width_person = 70)
        self.inicio_tarefa = Drop_new([i for i in range(30,301)], inicio, width_person = 70)
        self.fim_tarefa = Drop_new([i for i in range(30,311)], fim, width_person = 70)
        self.passo_tarefa = Drop_new([0,0.1,0.3,0.5,0.7,0.9]+[i for i in range(1,20)], passo, width_person = 70)



    def build(self):
        remover_tarefa = ft.IconButton(icon_color ='blue',icon=ft.icons.DELETE, on_click = self.clicked, data ='del', icon_size = 18)
        self.play_parefa = ft.IconButton(icon_color ='blue',icon=ft.icons.PLAY_ARROW, on_click = self.clicked, data ='play tarefa', icon_size = 18)
        pause_parefa = ft.IconButton(icon_color ='blue',icon=ft.icons.PAUSE, on_click = self.clicked, data ='pause tarefa', icon_size = 18)

        linha_tarefa = [
            remover_tarefa,
            self.nome_tarefa,
            self.duracao_tarefa,
            self.inicio_tarefa,
            self.fim_tarefa,
            self.passo_tarefa,
            self.play_parefa,
            pause_parefa
        ]
        linha_tarefa = ft.Row([Container_new2(i, 10,30,1) for i in linha_tarefa], tight=True, spacing=0,alignment='center', expand=1)
        
        return Container_new2(linha_tarefa, 10)
    
    def clicked(self, e):
        self.task_delete(self,e)

class New_task(ft.Row):
    def __init__(self,
        task_delete,
        nome='',
        duracao=3,
        inicio=70,
        fim=170,
        passo = 1,
        ):
        super().__init__()
        self.task_delete = task_delete
        self.nome_tarefa = ft.TextField(hint_text = 'nome da tarefa', width = 280, capitalization = TextCapitalization.CHARACTERS, value = nome, height=25, fill_color= 'white,0.1',content_padding=7,border_width = 0,dense=True)
        self.duracao_tarefa = Display(value = duracao,opitions=[0.1,0.3,0.5]+[i for i in range(1,31)], width = 60,height= 25,text_size = 13,borda_width = 0.5, border_radius=5)
        self.inicio_tarefa = Display(value = inicio,opitions=[i for i in range(30,301)], width = 60,height= 25,text_size = 13,borda_width = 0.5, border_radius=5)
        # self.inicio_tarefa = Drop_new([i for i in range(30,301)], inicio, width_person = 70)
        self.fim_tarefa = Display(value = fim,opitions=[i for i in range(30,311)], width = 60,height= 25,text_size = 13,borda_width = 0.5, border_radius=5)
        self.passo_tarefa = Display(value = passo,opitions=[0,0.1,0.3,0.5,0.7,0.9]+[i for i in range(1,20)], width = 60,height= 25,text_size = 13,borda_width = 0.5, border_radius=5)
        # self.fim_tarefa = Drop_new([i for i in range(30,311)], fim, width_person = 70)
        # self.passo_tarefa = Drop_new([0,0.1,0.3,0.5,0.7,0.9]+[i for i in range(1,20)], passo, width_person = 70)

        self.tight=True,
        self.spacing=0
        self.alignment='center' 
        self.expand=0


        remover_tarefa = ft.IconButton(icon_color ='blue',icon=ft.icons.DELETE, on_click = self.clicked, data ='del', icon_size = 18)
        self.play_parefa = ft.IconButton(icon_color ='blue',icon=ft.icons.PLAY_ARROW, on_click = self.clicked, data ='play tarefa', icon_size = 18)
        pause_parefa = ft.IconButton(icon_color ='blue',icon=ft.icons.PAUSE, on_click = self.clicked, data ='pause tarefa', icon_size = 18)

        linha_tarefa = [
            remover_tarefa,
            self.nome_tarefa,
            self.duracao_tarefa,
            self.inicio_tarefa,
            self.fim_tarefa,
            self.passo_tarefa,
            self.play_parefa,
            pause_parefa
        ]
        # linha_tarefa = ft.Row([Container_new2(i, 10,30,1) for i in linha_tarefa], tight=True, spacing=0,alignment='center', expand=1)
        self.controls = [i for i in linha_tarefa]
        
        # return Container_new2(linha_tarefa, 10)
    
    def clicked(self, e):
        self.task_delete(self,e)

class Slider_new(ft.UserControl):
    def __init__(self,
                texto = None,
                 min = None,
                 max = None,
                 divisions = None,
                 fator = 1, #valor a ser multiplicado por value
                 digitos = 1,
                 width = 200,
                 on_change = None,
                 data = None, 
                 value = False,
    ):



        super().__init__()
        self.texto = texto
        self.min = min
        self.max = max
        self.divisions = divisions
        self.fator = fator
        self.digitos = digitos
        self.width = width
        self.on_change = on_change
        self.data = data
        self.value = value

        self.passo_fim2 = ft.Slider(active_color = '#004499',thumb_color = '#333333',min = self.min, 
                                 max = self.max, divisions=self.divisions,value = self.value, 
                                 width=self.width,on_change=self.mudou, data = self.data)
        valor = round(self.passo_fim2.value*self.fator,self.digitos)
        if self.digitos == 0:
            valor = int(valor)
        self.texto2 = ft.Text(f'{self.texto} ({valor})')

    def mudou(self,e):
        valor = round(self.passo_fim2.value*self.fator,self.digitos)
        if self.digitos == 0:
            valor = int(valor)
        self.texto2.value = f'{self.texto} ({valor})'
        self.value = valor
        self.on_change(e, self)
        self.update()

    def build(self):
        return ft.Row([self.texto2, self.passo_fim2],alignment='start', tight = True, spacing=0,run_spacing = 0, height=30 )

    @property
    def getvalue(self):
        return self.passo_fim2.value
    @getvalue.setter
    def setvalue(self, valor):
        self.passo_fim2.value = valor
        self.value = valor
        valor2 = round(self.passo_fim2.value*self.fator,self.digitos)
        if self.digitos == 0:
            valor2 = int(valor2)
        self.texto2.value = f'{self.texto} ({valor2})'
        self.update()

# class Slider_new2(ft.UserControl):
#     def __init__(self,
#                 texto = None,
#                  min = None,
#                  max = None,
#                  divisions = None,
#                  fator = 1, #valor a ser multiplicado por value
#                  digitos = 1,
#                  width = None,
#                  on_change = None,
#                  data = None, 
#                  value = False,
#                  col1 = 4,
                
#     ):
#         super().__init__()
#         self.texto = texto
#         self.min = min
#         self.max = max
#         self.divisions = divisions
#         self.fator = fator
#         self.digitos = digitos
#         self.width = width
#         self.on_change = on_change
#         self.data = data
#         self.value = value
#         self.col1 = col1


#         self.texto2 = ft.Text(f'{self.texto}', no_wrap = True)
#         self.passo_fim2 = ft.Slider(min = self.min, active_color = '#004499',thumb_color = '#333333',
#                                  max = self.max, value = self.value, 
#                                 on_change=self.mudou, data = self.data,  col = 12-self.col1)
#         self.caixa = ft.TextField(value = f'{self.passo_fim2.value:.0f}', border_width = 1, width=50,height=45, dense=True , content_padding = 5,
#                                text_align = "center", on_change = self.mudou2,)
        


#     def mudou(self,e):
#         # self.texto2.value = f'{self.texto} ({self.passo_fim2.value:.0f})'
#         if self.digitos == 0:
#             self.passo_fim2.value = int(self.passo_fim2.value)
#         else:
#             self.passo_fim2.value = round(float(self.passo_fim2.value), self.digitos)

#         self.caixa.value = f'{self.passo_fim2.value}'
#         if self.on_change != None:
#             self.on_change(e, self)
#         self.value = self.passo_fim2.value
#         self.update()
#     def mudou2(self,e):
#         # self.texto2.value = f'{self.texto} ({self.passo_fim2.value:.0f})'
#         self.passo_fim2.value = self.caixa.value 
#         self.value = self.passo_fim2.value
#         if self.on_change != None:
#             self.on_change(e, self)
#         self.update()       

#     def build(self):
#         return ft.ResponsiveRow([ft.Row([self.texto2, self.caixa], col = self.col1),self.passo_fim2, ],expand = 0,alignment='start', spacing=0,run_spacing = 0, height=30,)#,alignment='start', tight = True, spacing=0,run_spacing = 0, height=30 

#     @property
#     def getvalue(self):
#         return self.passo_fim2.value
#     @getvalue.setter
#     def getvalue(self, valor):
#         self.passo_fim2.value = valor
#         self.value = valor
#         valor2 = round(self.passo_fim2.value,self.digitos)
#         if self.digitos == 0:
#             valor2 = int(valor2)
#         self.caixa.value = f'{valor}'
#         self.update()

class Slider_new4(ft.ResponsiveRow):
    def __init__(self,
                texto = None,
                 min = None,
                 max = None,
                 divisions = None,
                 fator = 1, #valor a ser multiplicado por value
                 digitos = 1,
                 width = None,
                 on_change = None,
                 data = None, 
                 value = False,
                 col1 = 4,
                 expand = 0,
                
    ):
        super().__init__()
        self.texto = texto
        self.min = min
        self.max = max
        self.divisions = divisions
        self.fator = fator
        self.digitos = digitos
        self.width = width
        self.on_change = on_change
        self.data = data
        self.value = value
        self.col1 = col1
        self.texto2 = ft.Text(f'{self.texto}', no_wrap = True)

        self.passo_fim2 = ft.Slider(min = self.min, active_color = '#004499',thumb_color = '#333333',
                                 max = self.max, value = self.value, 
                                on_change=self.mudou, data = self.data,  col = 12-self.col1)
        if self.digitos == 0:
            valor = f'{self.passo_fim2.value:.0f}'
        else:
            valor = f'{self.passo_fim2.value:.1f}'

        self.caixa = ft.TextField(value = valor, border_width = 1, width=50,height=45, dense=True , content_padding = 5,
                               text_align = "center", on_change = self.mudou2,)
        
        self.expand = expand
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.spacing=0
        self.run_spacing = 0 
        self.height=30
        self.controls = [ft.Row([self.texto2, self.caixa], col = self.col1),self.passo_fim2, ]

    def colu(self, x=2):
        return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}
       

    def mudou(self,e):
        # self.texto2.value = f'{self.texto} ({self.passo_fim2.value:.0f})'
        if self.digitos == 0:
            self.passo_fim2.value = int(self.passo_fim2.value)
        else:
            self.passo_fim2.value = round(float(self.passo_fim2.value), self.digitos)

        self.caixa.value = f'{self.passo_fim2.value}'
        if self.on_change != None:
            self.on_change(e, self)
        self.value = self.passo_fim2.value
        self.update()
    def mudou2(self,e):
        # self.texto2.value = f'{self.texto} ({self.passo_fim2.value:.0f})'
        self.passo_fim2.value = self.caixa.value 
        self.value = self.passo_fim2.value
        if self.on_change != None:
            self.on_change(e, self)
        self.update()       



    @property
    def getvalue(self):
        return self.passo_fim2.value
    @getvalue.setter
    def getvalue(self, valor):
        self.passo_fim2.value = valor
        self.value = valor
        valor2 = round(self.passo_fim2.value,self.digitos)
        if self.digitos == 0:
            valor2 = int(valor2)
        self.caixa.value = f'{valor}'
        self.update()

class Saidas(ft.UserControl):
    def __init__(self,
        texto1 = '',
        texto2 = '',
        texto3 = '',
        texto4 = '',
        texto5 = '',
        texto6 = '',  
        cor = 'white',
        size = 20,                              
                  ):
        super().__init__()
        # self.t1 = texto1
        # self.t2 = texto2
        # self.t3 = texto3
        # self.t4 = texto4
        # self.t5 = texto5
        # self.t6 = texto6
        self._texto1a = ft.Text(texto1, color = cor, size = size, visible=False)
        self._texto2a = ft.Text(texto2, color = cor, size = size, visible=False)
        self._texto3a = ft.Text(texto3, color = cor, size = size, visible=False)
        self._texto4a = ft.Text(texto4, color = cor, size = size, visible=False)
        self._texto5a = ft.Text(texto5, color = cor, size = size, visible=False)
        self._texto6a = ft.Text(texto6, color = cor, size = size, visible=False)
        self.Visibles(                
                 texto1,
                 texto2,
                 texto3,
                 texto4,
                 texto5,
                 texto6
                 )
      
    def build(self):
        self.saida = ft.Row(
            alignment= ft.MainAxisAlignment.START,
            vertical_alignment = 'center',
            
            # height=300,
            tight = True,
            wrap = True,
            expand=1,
            run_spacing = 2,
            # runs_count=1,
            # max_extent=300,
            # child_aspect_ratio=8,
            # spacing=1,
            # run_spacing=10,
            # padding = 0, 
            controls=[
                        self._texto1a, self._texto2a, self._texto3a,self._texto4a,self._texto5a,self._texto6a
                    #   ft.Column([self._texto1a, self._texto2a, self._texto3a],alignment = ft.MainAxisAlignment.START),
                    #   ft.Column([self._texto4a,self._texto5a,self._texto6a],alignment = ft.MainAxisAlignment.START),
                    #   ft.Row([],alignment = ft.MainAxisAlignment.SPACE_AROUND),  
                                     
                      ],                                            
        )
        # self.saida = ft.Container(self.saida, margin=margin.all(6))
        
        return self.saida
    
    def Visibles(self,                 
                 texto1,
                 texto2,
                 texto3,
                 texto4,
                 texto5,
                 texto6
                 ):
        if texto1 != '':
            self._texto1a.visible = True
        if texto2 != '':
            self._texto2a.visible = True
        if texto3 != '':
            self._texto3a.visible = True
        if texto4 != '':
            self._texto4a.visible = True
        if texto5 != '':
            self._texto5a.visible = True
        if texto6 != '':
            self._texto6a.visible = True 
    
      
    @property
    def texto1(self):       
        return self._texto1a.value
    
    @texto1.setter
    def texto1(self, texto):
        self._texto1a.value = texto 
        self._texto1a.size = 20
        self._texto1a.visible = True 
        self._texto1a.no_wrap = True
  
    @texto1.setter
    def texto1_color(self, color):
        self._texto1a.color = color
    @texto1.setter
    def texto1_size(self, size):
        self._texto1a.size = size 
    
    @property
    def texto2(self):       
        return self._texto2a.value
    
    @texto2.setter
    def texto2(self, texto):
        self._texto2a.value = texto 
        self._texto2a.size = 20
        self._texto2a.visible = True 
        self._texto2a.no_wrap = True
  
    @texto2.setter
    def texto2_color(self, color):
        self._texto2a.color = color
    @texto2.setter
    def texto2_size(self, size):
        self._texto2a.size = size 
    
    @property
    def texto3(self):       
        return self._texto3a.value
    
    @texto3.setter
    def texto3(self, texto):
        self._texto3a.value = texto 
        self._texto3a.size = 20
        self._texto3a.visible = True 
        self._texto3a.no_wrap = True
  
    @texto3.setter
    def texto3_color(self, color):
        self._texto3a.color = color
    @texto3.setter
    def texto3_size(self, size):
        self._texto3a.size = size 
    
    @property
    def texto4(self):       
        return self._texto4a.value
    
    @texto4.setter
    def texto4(self, texto):
        self._texto4a.value = texto 
        self._texto4a.size = 20
        self._texto4a.visible = True 
        self._texto4a.no_wrap = True
  
    @texto4.setter
    def texto4_color(self, color):
        self._texto4a.color = color
    @texto4.setter
    def texto4_size(self, size):
        self._texto4a.size = size 
    
    @property
    def texto5(self):       
        return self._texto5a.value
    
    @texto5.setter
    def texto5(self, texto):
        self._texto5a.value = texto 
        self._texto5a.size = 20
        self._texto5a.visible = True 
        self._texto5a.no_wrap = True
  
    @texto5.setter
    def texto5_color(self, color):
        self._texto5a.color = color
    @texto5.setter
    def texto5_size(self, size):
        self._texto5a.size = size 
    
    @property
    def texto6(self):       
        return self._texto6a.value
    
    @texto6.setter
    def texto6(self, texto):
        self._texto6a.value = texto 
        self._texto6a.size = 20
        self._texto6a.visible = True 
        self._texto6a.no_wrap = True
  
    @texto6.setter
    def texto6_color(self, color):
        self._texto6a.color = color
    @texto6.setter
    def texto6_size(self, size):
        self._texto6a.size = size 

class Saidas2(ft.UserControl):
    def __init__(self, 
                 texto1 = '',
                 texto2 = '',
                 texto3 = '',
                 texto4 = '',
                 texto5 = '',
                 texto6 = ''
                 ):
        super().__init__()

        self.texto1 = ft.Text(texto1, size = 20, visible=False)
        self.texto2 = ft.Text(texto1, size = 20, visible=False)
        self.texto3 = ft.Text(texto1, size = 20, visible=False)
        self.texto4 = ft.Text(texto1, size = 20, visible=False)
        self.texto5 = ft.Text(texto1, size = 20, visible=False)
        self.texto6 = ft.Text(texto1, size = 20, visible=False)
        self.Visibles(                
                 texto1,
                 texto2,
                 texto3,
                 texto4,
                 texto5,
                 texto6
                 )
    def build(self):
        self.saida = ft.Row(
            alignment= ft.MainAxisAlignment.START,
            vertical_alignment = 'center',
            
            # height=300,
            tight = True,
            wrap = True,
            expand=1,
            run_spacing = 2,
            # runs_count=1,
            # max_extent=300,
            # child_aspect_ratio=8,
            # spacing=1,
            # run_spacing=10,
            # padding = 0, 
            controls=[
                      self.texto1,self.texto2,self.texto6o3,
                      self.texto4,self.texto5,self.texto6
                    #   ft.Row([],alignment = ft.MainAxisAlignment.SPACE_AROUND),  
                                     
                      ],                                            
        )
        # self.saida = ft.Container(self.saida, margin=margin.all(6))
        
        return self.saida

    def Visibles(self,                 
                 texto1 ,
                 texto2,
                 texto6o3,
                 texto6o4,
                 texto6o5,
                 texto6
                 ):
        if texto1 != '':
            self.texto1.visible = True
        if texto2 != '':
            self.texto2.visible = True
        if texto6o3 != '':
            self.texto3.visible = True
        if texto6o4 != '':
            self.texto4.visible = True
        if texto6o5 != '':
            self.exto5.visible = True
        if texto6 != '':
            self.texto6.visible = True                                                            



    '''
class Pomodoro(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.pomodoro_control_thread = True
        self.tempo_pomodoro_set = 0.1
        self.Metro_normal = Metronomo()
        self.Metro_normal.pause = False
        self.parar = False
        self.tempo_descanso_value = 6
        self.quado_saida = ft.Row()
        self.saida_respiro = ft.Column(visible=False)



    def did_mount(self):
        self.Pomodoro()

    def build(self):
        return  ft.Row([self.quado_saida, self.saida_respiro])  
    def Pomodoro(self):
        texto = 'Pomodoro inciado...'
        self.quado_saida.visible = True        
        self.quado_saida.controls = [ft.Text(texto)]
        super().update()

        while self.pomodoro_control_thread:
            self.quado_saida.visible = True
            
            segundos = self.tempo_pomodoro_set*60
            while segundos >= 0:
                h, mins = divmod(segundos, 60*60)
                mins, secs = divmod(mins, 60)
                h, mins, secs = int(h), int(mins), int(secs)
                if texto != '':
                    contador = "{:s} {:02d}:{:02d}:{:02d}".format(texto,h, mins, secs)
                else:
                    contador = "{:02d}:{:02d}:{:02d}".format(h, mins, secs)

                self.quado_saida.controls = [ft.Text(contador)]
                sleep(1)
                super().update()
                segundos -= 1
                while self.Metro_normal.pause:
                    sleep(0.3)
                if self.parar or not self.pomodoro_control_thread:
                    break

            if self.parar or not self.pomodoro_control_thread:
                self.quado_saida.visible = False
                self.quado_saida.controls = None
                break

            MessageBeep(MB_ICONHAND)

            self.Respiro()
            
            if not self.pomodoro_control_thread:
                break
            MessageBeep(MB_ICONHAND)

            if not self.pomodoro_control_thread:
                break
            texto = 'Volte a treinor por '

        self.quado_saida.controls =  None

    def Respiro(self):
        # self.Metro_normal.pause = True
        # estado_saida_treinamento = self.saida_treinamento.visible
        # estado_saida_quado = self.quado_saida.visible
        # self.saida_treinamento.visible = False
        self.quado_saida.visible = False
        self.saida_respiro.visible = True
        descan = int(self.tempo_descanso_value*60/19.4)
        # print(descan)
        # self.Metro_normal.pause = False
        self.parar = False
        width_max = 740
        respiro = ft.Container(content=ft.Text(),bgcolor= ft.colors.YELLOW,width = 0, border_radius=40)
        def Inspire(d):
            # self.quado_saida.content = ft.Text(f'INSPIRE ({d})')
            s = Saidas(f'INSPIRE ({d})', cor = ft.colors.YELLOW, size = 50)
            # s.saida_tempo_de_treino.visible = True
            # self.saida.texto1_size = 50
            # self.saida.texto1_color= ft.colors.YELLOW
            self.saida_respiro.controls = [ft.Column([s, respiro])]
            # self.quado_saida.content.alignment= ft.MainAxisAlignment.CENTER

        def Expire(d):
            s = Saidas(f'EXPIRE  ({d})', cor = ft.colors.GREEN, size = 50)

            # s.saida_tempo_de_treino.visible = True
            # self.saida.texto1_size = 50
            # self.saida.texto1_color= ft.colors.GREEN
            self.saida_respiro.controls = [ft.Column([s, respiro])]
            # self.quado_saida.content.alignment= ft.MainAxisAlignment.CENTER


        for d in range(descan,0,-1):
            a = time()
            Inspire(d)
            super().update()
            for i in range(0,width_max,6*2):
                respiro.width = i
                sleep(0.001)
                if self.parar:
                    break
                super().update()
            respiro.bgcolor = ft.colors.GREEN
            Expire(d)
            super().update()
            if self.parar:
                break             
            for i in range(width_max,0,-1*2):
                respiro.width = i
                if self.parar:
                    break                    
                sleep(0.01567)
                super().update()
            respiro.bgcolor = ft.colors.YELLOW
            b = time()-a
            print(b)

        # self.saida_treinamento.visible = estado_saida_treinamento
        # self.quado_saida.visible = estado_saida_quado
        # self.saida_respiro.controls = None
        self.saida_respiro.visible = False
        self.quado_saida.visible = True
        self.Metro_normal.pause = False
        respiro.width = 0
        super().update()
    '''

class SaveSelectFile(ft.UserControl):
    def __init__(self, tipo = 'txt'):
        super().__init__()
        self.tipo = tipo
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.nome_arquivo = None
        self.func = None

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        match self.func:
            case 'select':
                self.nome_arquivo = f'{e.files[0].path}'
            case 'save':
                self.nome_arquivo = f'{e.path}.{self.tipo}'
            case 'select_pasta':
                self.nome_arquivo = f'{e.path}'

        super().update()

        
    # @property
    def Save(self):
        self.func = 'save'
        self.pick_files_dialog.save_file(file_type = ft.FilePickerFileType.CUSTOM, allowed_extensions = [self.tipo])
        while not self.nome_arquivo:
            sleep(0.3)
        self.update()
        return self.nome_arquivo
    
    def Select(self, tipo = None):
        self.nome_arquivo = None
        if tipo not in [None, '']:
            self.tipo = tipo
        self.func = 'select'
        self.pick_files_dialog.pick_files(file_type = ft.FilePickerFileType.CUSTOM, allowed_extensions = [self.tipo])
        while self.nome_arquivo == None:
            sleep(0.3)
        self.update()
        return self.nome_arquivo  


    def Select_pasta(self):        
        self.func = 'select_pasta'
        self.pick_files_dialog.get_directory_path(dialog_title = 'selecione a pasta')
        while not self.nome_arquivo:
            sleep(0.3)
        self.update()
        return self.nome_arquivo            
    
    def build(self):
        return self.pick_files_dialog 
    
# class Container_new3(ft.UserControl):
#     def __init__(self,
#                  content = None, 
#                  gradiente = ('black', 'white'),
#                  height = None,
#                  scale = 1,
#                  border_radius = None,
#                  rotação = 0.3,
#                  ShadowColor = 'blue,0.6',
#                  page = None,
                
#         ):
#         super().__init__()
#         self.page = page
#         self.content = content
#         self.gradiente = gradiente
#         self.height = height
#         self.scale = scale
#         self.border_radius = border_radius
#         self.rot = rotação
#         self.ShadowColor = ShadowColor

#         self.horizontal = ft.BorderSide(3, ft.colors.with_opacity(0.4,'blue'))
#         self.vertical = ft.BorderSide(3, ft.colors.with_opacity(0.9,'gray'))
        
#         self.bor = ft.Border(left=self.horizontal, top=self.horizontal, right=self.vertical, bottom=self.vertical)
#         self.bor = ft.border.all(5, ft.colors.with_opacity(0.3,'red'))
    
#         self.sombra =  ft.BoxShadow(
#             spread_radius=0,
#             blur_radius=15,
#             color=self.ShadowColor,
#             offset=ft.Offset(3, 3),
#             blur_style=ft.ShadowBlurStyle.NORMAL)  


#         self.gradient =  gradient=ft.LinearGradient(
#             begin=ft.Alignment(0, 1),
#             end=ft.Alignment(0, -1),
            
#             colors=[
#                 self.gradiente[0],
#                 self.gradiente[0],
#                 self.gradiente[0],
#                 self.gradiente[0],
#                 self.gradiente[0],
#                 self.gradiente[1],
#                         ],
#             tile_mode=ft.GradientTileMode.MIRROR,
#             rotation=self.rot*3.14/180,
#         )
#         self.saida = ft.Container(content=self.content,   
#                          border=self.bor, 
#                          shadow = self.sombra, 
#                          scale = self.scale, 
#                          height = self.height,
#                          border_radius = self.border_radius,
#                          gradient=self.gradient, 
#                          padding = 0
#                          )
#     def build(self):
#         return self.saida


class BotaoC(ft.Container):
    def __init__(self,texto = '', color  = 'blue', data = None, scale = 1, on_click = None,height = 30, width = None,border_radius =20,gradiente = ("black", "#777777")):
        super().__init__()
        self.content = ft.TextButton(
            content = ft.Text(
                    texto, 
                    size=20, 
                    weight='bold', 
                    no_wrap=True, 
                    color=color),
            data = data,on_click=on_click, 
            width = width,height = height)
        
        self.scale = scale
        self.border = ft.border.all(5, ft.colors.with_opacity(0.3,'red'))
        self.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=15,
                    color=ft.colors.with_opacity(0.6,'blue'),
                    offset=ft.Offset(3, 3),
                    blur_style=ft.ShadowBlurStyle.NORMAL
            )   
        self.border_radius = border_radius
        self.gradient = ft.LinearGradient(
                begin=ft.Alignment(0, 1),
                end=ft.Alignment(0, -1),
                
                colors=[
                    gradiente[0],
                    gradiente[0],
                    gradiente[0],
                    gradiente[0],
                    gradiente[0],
                    gradiente[1],
                            ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=0*3.14/180,
            )
        self.padding = 0


class Container_new2C(ft.Container):
    def __init__(self,
            content = None,
            border_radius =20, 
            height = None, 
            scale = None, 
            gradiente = ("black", "#777777"), 
            col = None,
            expand = 0
        ):
        super().__init__()
        self.content=content   
        self.border=ft.border.all(5, ft.colors.with_opacity(0.3,'red'))
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.colors.with_opacity(0.6,'blue'),
            offset=ft.Offset(3, 3),
            blur_style=ft.ShadowBlurStyle.NORMAL) 
        self.scale = scale 
        self.height = height
        self.border_radius = border_radius
        self.gradient=ft.LinearGradient(
            begin=ft.Alignment(0, 1),
            end=ft.Alignment(0, -1),
            
            colors=[
                gradiente[0],
                gradiente[0],
                gradiente[0],
                gradiente[0],
                gradiente[0],
                gradiente[1],
                        ],
            tile_mode=ft.GradientTileMode.MIRROR,
            rotation=0*3.14/180)
        self.padding = 0 
        self.col = col   
        self.expand =  expand   




def Container_new2(i, border_radius =20, height = None, scale = None, gradiente = ("black", "#777777"), col = None):
    horizontal = ft.BorderSide(3, ft.colors.with_opacity(0.4,'blue'))
    vertical = ft.BorderSide(3, ft.colors.with_opacity(0.9,'gray'))
    
    bor = ft.Border(left=horizontal, top=horizontal, right=vertical, bottom=vertical)
    bor = ft.border.all(5, ft.colors.with_opacity(0.3,'red'))
    
    sombra =  ft.BoxShadow(
        spread_radius=0,
        blur_radius=15,
        color=ft.colors.with_opacity(0.6,'blue'),
        offset=ft.Offset(3, 3),
        blur_style=ft.ShadowBlurStyle.NORMAL)        
    gradiente =  ft.LinearGradient(
        begin=ft.Alignment(0, 1),
        end=ft.Alignment(0, -1),
        
        colors=[
            gradiente[0],
            gradiente[0],
            gradiente[0],
            gradiente[0],
            gradiente[0],
            gradiente[1],
                    ],
        tile_mode=ft.GradientTileMode.MIRROR,
        rotation=0*3.14/180,
    )
    return ft.Container(content=i,   border=bor, shadow = sombra, scale = scale, height = height,border_radius = border_radius,gradient=gradiente, padding = 0, col = col)

# def Botao( texto = None,  icon = None,size = 30,width = 80, height = 30,on_click = None, data = None, color  = 'blue', rot = 30, gradiente = ("black", "#777777")):   
#     return Container_new2(ft.TextButton(content = ft.Text(texto, size=20, weight='bold', no_wrap=True, color=color), data = data,on_click=on_click, 
#                                      width = width,height = height), gradiente = gradiente   )

def Botao2( texto = None,  icon = None,size = 30,width = 80, height = 50,on_click = None, data = None, color  = 'blue', rot = 30):
    bor2 = ft.border.BorderSide(20, ft.colors.with_opacity(1,color))
    bor = ft.border.all(0, ft.colors.with_opacity(0.3,'#995555')) 
    sombra =  ft.BoxShadow(
        spread_radius=0,
        blur_radius=30,
        color=ft.colors.with_opacity(0.6,color),
        offset=ft.Offset(3, 3),
        blur_style=ft.ShadowBlurStyle.NORMAL)
    gradiente =  gradient=ft.LinearGradient(
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(-0.1, -0.1),
        
        colors=[
            "#777777",
            "#000000",
            "#000000",
                    ],
        tile_mode=ft.GradientTileMode.MIRROR,
        rotation=rot*3.14/180,
    )


    if icon == None:
        conteudo = ft.ElevatedButton(content = ft.Text(texto, size=25, weight='bold', no_wrap=True, color=color),bgcolor = ft.colors.with_opacity(0,'black'))
    else:
        conteudo = ft.Icon(icon, color=color)
    return ft.Container( 
        content= conteudo,
            # [
                # ft.Text("1", color=ft.colors.WHITE),
                # ft.Text("2", color=ft.colors.WHITE, right=0),
                # ft.Text("3", color=ft.colors.WHITE, right=0, bottom=0),
                # ft.Text("4", color=ft.colors.WHITE, left=0, bottom=0),
            # ]
        # ),
        # top = 5,
        alignment=ft.Alignment(0, 0),
        bgcolor='green',
        width=width,
        height=height,
        # height=220,
        border_radius=15,
        on_click = on_click,
        shadow=sombra,
        gradient=gradiente,
        border= bor, 
        data = data,    
            

        )


def Slider_new3(texto,min = 10, max = 240, width=150 ):
    return ft.Row([ft.Row([ft.Text(texto),ft.Slider(min = min, max = max, width=width,active_color = '#004499',thumb_color = '#333333',)])],alignment='start', tight = True, spacing=0,run_spacing = 0, height=30 )

def main_test(page: ft.Page):
    page.window.width = 1500
    page.window.height = 750


    t = Contador(3600, cor= 'blue', size = 15)
    # t.continuar_treinando = True
    def Parar(e):
        t.segundos = int(b.value)
    b = TextField( on_submit=Parar)

    def atualizar(e,slider):
        # Tempo_de_estudo = Slider_new2('Tempo de estudo', 10, 240,data = 'Tempo_de_estudo', width=200, value = 10, on_change = atualizar).bunda()
        # print(slider)
        page.update()
   
    # Tempo_de_estudo = Slider_new2('Tempo de estudo', 0, 5.0,data = 'Tempo_de_estudo', value = 4.3, on_change = atualizar, col1=2)
    # Tempo_de_estudo = ft.Row([ft.Text('asldjfshldkajl'),ft.Slider(min = 10, max = 240, width=350)])
    # Tempo_de_estudo = Slider_new3('casa', 10,250,130)
    # Tempo_de_estudo = ft.ResponsiveRow([
    # ft.Column(col=6, controls=[ft.Text("Column 1")]),
    # ft.Column(col=6, controls=[ft.Text("Column 2")])
    # ])
    largura  = ft.Text()
    def page_resize(e):
        # print("New page size:", page.window_width, page.window_height)
        # print("New page size:", page.window_width, page.window_height)
        # print("New page size:", page.window_width, page.window_height)
        largura.value = page.window.width
        sleep(5)
        page.update()


    page.on_resized = page_resize
    page.on_close = page_resize

    def aaa(e):
        pass
            
    # conta = Container_new3(content = ft.Text('casadas'), border_radius = 15, rotação=50, ShadowColor='blue,0.2')

    conta2 = ft.TextButton('01', on_click=aaa)

    # tab = Tabs_new(tabs = [['tab1',ft.Column([ft.Text('meu ovo')])], ['tab2',ft.Column([ft.Text('minha pica')])]])
    # tab.set_height = 500
    # tab.set_width = 400
    # tab.Add_tab(('buceta',ft.Container(ft.Column([ft.Row([ft.Text('aoisdoaijsdoij')])]))),('tab1',ft.Column([ft.Text('meu ovo')])))
    
    tab = Classificador()

    page.add(tab)
    page.update()



if __name__ == '__main__':
    ft.app(target=main_test)            
