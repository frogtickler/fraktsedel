import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import glob
from PIL import BdfFontFile
from PIL import PcfFontFile
from barcode import EAN13
from barcode.writer import ImageWriter


st.header('Skapa en fraktsedel enkelt och gratis') 



st.set_page_config(page_title="Fraktssedel", layout="wide")

col1, col2 = st.columns(2)

#Fraktsedel nummer
frakstsedelnr = st.text_input('Fraktsedelnummer', placeholder="fraktsedelnummer")

#Avsändar info
with col1:
    Avsandare_namn = st.text_input('Avsändaren namn:', placeholder='företag/privatperson namn')
    Avsandare_andress = st.text_input('Avsändaren adress:', placeholder='Adress')
    Avsandare_referensnummer = st.text_input('Avsändaren referensnummer:', placeholder='referensnummer')
    av_stad = st.text_input('Avsändare: Stad', placeholder="ort")
    av_postkod = st.text_input('Avsändare: postkod', placeholder="postkod")
    av_port = st.text_input('Avsändare: portkod', placeholder="portkord")
    av_orgnummer = st.text_input('Avsändare: organisationsnummer', placeholder="organisationsnummer")
    av_kontakt = st.text_input('Avsändare: kontakt', placeholder="kontakt")
    av_datum = st.text_input('Avsändare: datum', placeholder="datum")
#mottagar info
with col2:
    mottagare_namn = st.text_input('Mottagarens namn:', placeholder='företag/privatperson namn')
    mottagare_adress = st.text_input('Mottagarens adress:', placeholder='Adress')
    mottagare_referensnummer = st.text_input('Mottagare referensnummer:', placeholder='Mottagare referensnummer')
    lev_stad = st.text_input('Leverans: Stad', placeholder="ort")
    lev_postkod = st.text_input('Leverans: postkod', placeholder="postkod")
    lev_port = st.text_input('Leverans: portkod', placeholder="portkord")
    lev_va = st.text_input('Leverans: våning', placeholder="våning")
    lev_kontakt = st.text_input('Leverans kontakt', placeholder="kontakt")
    lev_tel = st.text_input('Leverans: telefonnummer', placeholder="telefonnummer")
#tull info
innehal = st.text_input('Innehåll, för tullen samt för känsliga ämnen:', 'innehåll')

#ömtåligt gods
omtoligt = st.radio(
    "Innehåller paketet ömtåligt gods?",
    ["***Ja***", "***Nej***"])

if omtoligt == '***Ja***':
   st.write('ja paketet innehåller ömtåligt gods')
   omttol="Ömtoligt gods"
else:
    st.write('Nej paketet innehåller ej ömtåligt gods')
    omttol=" "
#kollin

kollin = st.number_input("Antal kollin")
vikt = st.number_input('Vikt per kollin [kg]:')
vikt_tot = vikt * kollin
viktrund = round(vikt_tot,5)
st.write('Total vikt', viktrund)
vikttext = str(viktrund)

kollinslag = st.selectbox(
    'Kollingslag',
    ('paket', 'rör', 'påse'))

#volym

col3, col4 = st.columns(2)

with col3:
    langd = st.number_input("Paketets längd:", placeholder="Längd")
    hojd = st.number_input("Paketets höjd:", placeholder="Höjd")
    bredd = st.number_input("Paketets bredd:", placeholder="Bredd")

with col4:
    optionlangd = st.selectbox(
        'Enhet, längd',
        ('mm', 'cm', 'm'))

    optionhojd = st.selectbox(
    'Enhet, höjd',
    ('mm', 'cm', 'm'))

    optionbredd = st.selectbox(
    'Enhet, bredd',
    ('mm', 'cm', 'm'))


#Konvertera längd
if optionlangd == 'mm':
    langd = langd / 1000
   # st.write(langd_konvmm)

if optionlangd == 'cm':
    langd = langd / 100
   # st.write(langd_konvcm)

if optionlangd == 'm':
    langd = langd
   # st.write(langd_konvm)

# konvertera höjd
if optionhojd == 'mm':
    hojd = hojd / 1000
    #st.write(hojd_konvmm)

if optionhojd == 'cm':
    hojd = hojd / 100
   # st.write(hojd_konvcm)

if optionhojd == 'm':
    hojd = hojd
   # st.write(hojd_konvm)

#konvertera bredd
if optionbredd == 'mm':
    bredd = bredd / 1000
   # st.write(bredd_konvmm)

if optionbredd == 'cm':
    bredd = bredd / 100
   # st.write(bredd_konvcm)

if optionbredd == 'm':
    bredd = bredd
   # st.write(bredd_konvm)

volym = langd * hojd * bredd  # Omvandlade till meter
st.write('Volymen är ', round(volym,10), '[m^3]')
volymtext = str(round(volym,10))



# leveransanvingar

# betalning
betalning = st.text_input('Betalning', placeholder="Vem betalar fraktkostnaden?")

#frakt
frakt = st.text_input('Frakt/transportföretaget', placeholder="Namn på fraktbolaget")

#kundnr
kundnr = st.text_input('Kundnummer', placeholder="Kundnummer")

#fraktsedelnummer
fraktsedelnr = st.text_input('Fraksedelnummer', placeholder="(EAN13)")

width = 385
height = 725


if st.button('Print'):
    img = Image.new(mode = "RGB", size = (width, height), color="white")
    l1 = ImageDraw.Draw(img)
    


    #Avsändare info
    l1.text((5,5), "Från", fill=(0, 0, 0),)
    l1.text((5,20), Avsandare_namn, fill=(0, 0, 0), )
    l1.text((5,35), Avsandare_andress, fill=(0, 0, 0), )
    l1.text((5,50), "SE- ", fill=(0, 0, 0),)
    l1.text((30,50), av_postkod, fill=(0, 0, 0), )
    l1.text((5,65), av_stad, fill=(0, 0, 0), )

    #org. no kontakt, av-datum
    l1.text((250,5), "org.No: ", fill=(0, 0, 0), )
    l1.text((290, 5), av_orgnummer, fill=(0, 0, 0), )
    l1.text((250,20), "Kontakt: ", fill=(0, 0, 0), )
    l1.text((295, 20), av_kontakt, fill=(0, 0, 0), )
    l1.text((250,35), "AVS-datum: ", fill=(0, 0, 0), )
    l1.text((310, 35), av_datum, fill=(0, 0, 0), )
    #låda (x1,y2), (x2,y2)
    shape1 = [(5, 100), (5, 125)]
    shape2 = [(3, 100), (30, 100)]
    l1.line(shape1, fill =(0,0,0), width = 5)
    l1.line(shape2, fill =(0,0,0), width = 5)
    shape3 = [(380, 100), (353, 100)]
    shape4 = [(378, 100), (378, 127)]
    l1.line(shape3, fill =(0,0,0), width = 5)
    l1.line(shape4, fill =(0,0,0), width = 5)
    shape5 = [(5, 300), (5, 275)]
    shape6 = [(3, 300), (30, 300)]
    l1.line(shape5, fill =(0,0,0), width = 5)
    l1.line(shape6, fill =(0,0,0), width = 5)
    shape7 = [(380, 300), (353, 300)]
    shape8 = [(378, 275), (378, 300)]
    l1.line(shape7, fill =(0,0,0), width = 5)
    l1.line(shape8, fill =(0,0,0), width = 5)
    #referensnummer
    l1.text((13,320), "Avsändare-referensnummer: ", fill=(0, 0, 0))
    l1.text((160,320), Avsandare_referensnummer, fill=(0, 0, 0), )
    l1.text((13,305), "Mottagare-referensnummer: ", fill=(0, 0, 0))
    l1.text((160,305), mottagare_referensnummer, fill=(0, 0, 0))
    
    #streck1
    shape9 = [(5, 335), (380, 335)]
    l1.line(shape9, fill =(0,0,0), width = 5)
    #Frakt företag
    l1.text((13,350), frakt, fill=(0, 0, 0), )
    #kundnummer
    l1.text((13,370), "kundnr: ", fill=(0, 0, 0), )
    l1.text((60,370), kundnr, fill=(0, 0, 0), )
    #betalning
    l1.text((13,385), "fraktbetalning: ", fill=(0, 0, 0), )
    l1.text((105,385), betalning, fill=(0, 0, 0), )
    #TILLÄGG
    l1.text((13,400), "Tillägningsinformation: ", fill=(0, 0, 0), )
    l1.text((155,400), omttol, fill=(0, 0, 0), )
    #Mottagare info
   
    l1.text((15,105), "Till:", fill=(0, 0, 0), )
    l1.text((13,120), mottagare_namn, fill=(0, 0, 0), )
    l1.text((13,135), mottagare_adress, fill=(0, 0, 0), )
    l1.text((13,150), "SE- ", fill=(0, 0, 0),  )
    l1.text((45,150), lev_postkod, fill=(0, 0, 0), )
    l1.text((13,170), lev_stad, fill=(0, 0, 0), )
    l1.text((13,185), "Sweden", fill=(0, 0, 0), )
    l1.text((13,200), "Portkod: ", fill=(0, 0, 0), )
    l1.text((65,200), lev_port, fill=(0, 0, 0), )
    l1.text((13,215), "Kontakt:", fill=(0, 0, 0), )
    l1.text((60, 215), lev_kontakt, fill=(0, 0, 0), )
    l1.text((13,230), "Tel:", fill=(0, 0, 0), )
    l1.text((35, 230), lev_tel, fill=(0, 0, 0), )
    l1.text((13,245), "Våning:", fill=(0, 0, 0), )
    l1.text((55,245), lev_va, fill=(0, 0, 0), )
    #streck2
    shape9 = [(5, 500), (380, 500)]
    l1.line(shape9, fill =(0,0,0), width = 5)
    l1.text((13,485), "Vikt [kg]: ", fill=(0, 0, 0), )
    l1.text((75,485), vikttext, fill=(0, 0, 0), )
    l1.text((13,470), "Volym [m^3]: ", fill=(0, 0, 0), )
    l1.text((85,470), volymtext, fill=(0, 0, 0), )
    # The number to be converted into a barcode
    # Skapa en EAN13-streckkod
    my_code = EAN13(fraktsedelnr, writer=ImageWriter())
    # Spara streckkoden som en PNG-bild
    my_code.save("new_code")
    barcode_bild = Image.open('new_code.png')
    slutlig_barcode = barcode_bild.resize((300,200), Image.BILINEAR)
    img.paste(slutlig_barcode, (42,510))
    # Visa den resulterande bilden
    col5, col6, col7 = st.columns(3)
    with col6:
        st.image(img, (385,725))









