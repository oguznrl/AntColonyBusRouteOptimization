import json
from math import ceil
from random import random
import flask
from flask import abort, jsonify ,request
from itertools import permutations


class Ilceler():
    def __init__(self,durak_isim,diger_ilceler,yolcu_say):
        self.durak_isim=durak_isim
        self.diger_ilceler=diger_ilceler
        self.yolcu_say=yolcu_say
class Karinca():
    def __init__(self,durak,sonlu_servis):
        self.durak=durak
        self.sonlu_servis=sonlu_servis 
        self.olasi_sonuclar=self.olasi_sonuclari_derle()
    def olasi_sonuclari_derle(self):
        olasi_sonuclar=list()
        if not self.sonlu_servis:
            yolcu_say=0
            servis_say=0
            for i in self.durak:
                yolcu_say+=i.yolcu_say
            if yolcu_say<=40:
                servis_say=1
            elif yolcu_say<=70:
                servis_say=2
            elif yolcu_say<=95:
                servis_say=3
            else:
                servis_say=ceil(((yolcu_say-95)/25)+3)
            per=list(permutations(self.durak,servis_say))
            for i in per:
                fark_dur=list()
                for j in self.durak:
                    if not j in i:
                        fark_dur.append(j)
                fark_dur_per=list(permutations(fark_dur,len(fark_dur)))
                for j in fark_dur_per:
                    iht=list()
                    for l in i:
                        iht.append([l])
                    for k in j:
                        min_mesafe=200
                        son_dur=Ilceler()
                        for l in i:
                            if l.diger_ilceler[k.durak_isim]<min_mesafe:
                                min_mesafe=l.diger_ilceler[k.durak_isim]
                                son_dur=l
                        iht[i.index(son_dur)].append(son_dur)
                    olasi_sonuclar.append(iht)
        else:
            for i in range(1,4):
                if len(self.durak)>3:
                    per=list(permutations(self.durak,i))
                    if i==1:
                        for j in per:
                            fark_dur=list()
                            for k in self.durak:
                                if k==j[0]:
                                    continue
                                else:
                                    fark_dur.append(k)
                            fark_dur_per=permutations(fark_dur,len(fark_dur))
                            for k in fark_dur_per:
                                ihtimal=list()
                                ihtimal.append([j[0]])
                                for l in k:
                                    ihtimal[0].append(l)
                                olasi_sonuclar.append(ihtimal)
                    else:
                        for j in per:
                            fark_dur=list()
                            for k in self.durak:
                                if not k in j:
                                    fark_dur.append(k)
                            fark_dur_per=permutations(fark_dur,len(fark_dur))
                            for k in fark_dur_per:
                                iht=list()
                                for l in j:
                                    iht.append([l])
                                for l in k:
                                    min_mesafe=200
                                    son_dur=Ilceler()
                                    for m in j:
                                        if m.diger_ilceler[l.durak_isim]<min_mesafe:
                                            min_mesafe=m.diger_ilceler[l.durak_isim]
                                            son_dur=m
                                    iht[j.index(son_dur)].append(m)
                                olasi_sonuclar.append(iht)
                else:
                    if i>len(self.durak):
                        break
                    else:
                        per=list(permutations(self.durak,i))
                        for j in per:
                            fark_dur=list()
                            for k in self.durak:
                                if not k in j:
                                    fark_dur.append(k)
                            fark_dur_per=permutations(fark_dur,len(fark_dur))
                            for k in fark_dur_per:
                                iht=list()
                                for l in j:
                                    iht.append([l])
                                for l in k:
                                    min_mesafe=200
                                    son_dur=Ilceler()
                                    for m in j:
                                        if m.diger_ilceler[l.durak_isim]<min_mesafe:
                                            min_mesafe=m.diger_ilceler[l.durak_isim]
                                            son_dur=m
                                    iht[j.index(son_dur)].append(m)
                                olasi_sonuclar.append(iht)
                                
        return olasi_sonuclar

#ilceleri_oku()


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def karinca_koloni(iterasyon_sayisi,rho,alpha,beta,ihtimallerin_maliyetleri):
    gecici_mal=ihtimallerin_maliyetleri
    toplam_maliyet=0
    gecici_mal.sort()
    yol_fer=[1]*yol_fer
    toplam_fer=0
    yerel_fer=[0]*len(ihtimallerin_maliyetleri)
    olasilik=[0]*len(ihtimallerin_maliyetleri)
    for i in gecici_mal:
        toplam_maliyet+=i
    for iter in range(iterasyon_sayisi):
        kumuletif_top=[0]*len(ihtimallerin_maliyetleri)
        kumuletif_deg=0
        if iter==0:
            for karinca in range(ihtimallerin_maliyetleri):
                yol_fer[karinca]+=1/ihtimallerin_maliyetleri[karinca]
            for i in range(len(yol_fer)):
                yol_fer[i]=yol_fer[i]*(1-rho)
            for i in range(len(yol_fer)):
                yerel_fer[i]=pow(yol_fer[i],alpha)*pow(gecici_mal[i],beta)
            for i in range(len(yol_fer)): 
                olasilik[i]=yerel_fer[i]/toplam_fer 
            for kum in range(len(olasilik)):
                kumuletif_deg+=olasilik[kum]
                kumuletif_top[kum]=kumuletif_deg
        else:
            for karinca in range(ihtimallerin_maliyetleri):
                random_deger=random()
                ind=0
                for kum in kumuletif_top:
                    if random_deger<kum:
                        ind=kumuletif_top.index(kum)
                        break
                yol_fer[karinca]+=1/ihtimallerin_maliyetleri[ind]
            for i in range(len(yol_fer)):
                yol_fer[i]=yol_fer[i]*(1-rho)
            for i in range(len(yol_fer)):
                yerel_fer[i]=pow(yol_fer[i],alpha)*pow(gecici_mal[i],beta)
            for i in range(len(yol_fer)): 
                olasilik[i]=yerel_fer[i]/toplam_fer 
            for kum in range(len(olasilik)):
                kumuletif_deg+=olasilik[kum]
                kumuletif_top[kum]=kumuletif_deg
    maks_yol=max(olasilik)
    return olasilik.index(maks_yol)

def maliyet_fonk(olasi_sonuclar,sonlumu):
    maliyet_list=list()
    for rotalar in olasi_sonuclar:
        yolcu_maliyet=0
        yol_maliyet=0
        servis_maliyet=0
        for ihtimal in rotalar:    
            for i in range(len(ihtimal)-1):                
                yol_maliyet+=ihtimal[i].diger_ilceler[ihtimal[i+1].durak_isim]
                yolcu_maliyet+=ihtimal[i].yolcu_sayisi
            yolcu_maliyet+=ihtimal[len(ihtimal)-1].yolcu_sayisi
            if len(ihtimal)>3:
                servis_maliyet=(len(ihtimal)-3)*50
        if sonlumu:
            maliyet_list.append(yol_maliyet*(1/yolcu_maliyet))
        else:
            maliyet_list.append(yol_maliyet+servis_maliyet)
    return maliyet_list

@app.route('/sinirli', methods=['POST'])
def sonlu_servis():
    sonuc={"rota":{

    }}
    
    if not request.json or not 'Durak' in request.json:
        abort(400)
    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
    json_object=json_object["Ilceler"]
    durak_json=json.loads(request.data)
    durak=list()
    for i in durak_json['Durak']:
        durak.append(Ilceler(i,json_object[i],durak_json['Durak'][i]))
    durak.append(Ilceler("Umuttepe",None,0))
    karinca=Karinca(durak,True)
    maliyet_list=maliyet_fonk(karinca.olasi_sonuclar)
    karinca_sonuc=karinca_koloni(20,0.5,0.2,0.5,maliyet_list)
    counter=0
    for i in karinca.olasi_sonuclar[karinca_sonuc]:
        sonuc['rota'][str(counter)]=[]
        for j in i:
            sonuc['rota'][str(counter)].append(j.isim)
    return jsonify(sonuc)

@app.route('/sinirsiz', methods=['POST'])
def sonsuz_servis():
    sonuc={"rota":{

    }}
    
    if not request.json or not 'Durak' in request.json:
        abort(400)
    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
    json_object=json_object["Ilceler"]
    durak_json=json.loads(request.data)
    durak=list()
    for i in durak_json['Durak']:
        durak.append(Ilceler(i,json_object[i],durak_json['Durak'][i]))
    durak.append(Ilceler("Umuttepe",None,0))
    karinca=Karinca(durak,False)
    maliyet_list=maliyet_fonk(karinca.olasi_sonuclar)
    karinca_sonuc=karinca_koloni(20,0.5,0.2,0.5,maliyet_list)
    counter=0
    for i in karinca.olasi_sonuclar[karinca_sonuc]:
        sonuc['rota'][str(counter)]=[]
        for j in i:
            sonuc['rota'][str(counter)].append(j.isim)
    return jsonify(sonuc)

app.run()

