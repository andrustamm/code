import streamlit as st


def render():
    st.header("Selgitused")
    st.write(
        "Kulude info pärineb CSV failidest, mida Telia jagab kliendile oma iseteenindusportaalis. \n"
        "Faild lisatakse Telia iseteenindusportaali arvete keskkonda, seal leiab need saki alt nimega 'Arve failina' ning lingi nimi, mille all on fail, on 'Teenuste eristus CSV'.\n\n"
        "Need CSV failid sisaldavad infot, mis on seotud kliendi poolt kasutatud teenuste, kasutusmahu ja ajaga.\n\n"
        "Failide struktuur on püsiv ja võimaldab lihtsat analüüsi.\n\n"
        "Peamised kategooriad, mida saab analüüsida, on:\n"
        "- **Kõned**: sisaldab infot kõneminutite kohta, mis on tehtud erinevate sidevahendite kaudu.\n"
        "- **Mobiilne internet**: sisaldab infot andmeside kasutamise kohta, mis on seotud erinevate sidevahenditega.\n"
        "- **Sõnumid**: sisaldab infot saadetud ja vastuvõetud sõnumite kohta.\n"
        "- **Parkimine**: sisaldab infot parkimisteenuse kasutamise kohta.\n"
        "Lihtsamaks andmeanalüüsiks olen lisanud üldised kategooriad, kategooriate määramine toimub regex reeglite abil, mis on defineeritud `config.py` failis. Need reeglid võimaldavad automaatselt määrata, millisesse kategooriasse konkreetne teenus kuulub, tuginedes teenuse nimele.\n\n"
        "Kasutaja saab valida erinevaid vaateid, et analüüsida andmeid erinevate kategooriate ja perioodide lõikes. Graafikud ja tabelid võimaldavad visualiseerida andmeid, et saada parem ülevaade teenuste kasutamisest ja kuludest."
    )