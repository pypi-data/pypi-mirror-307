import requests
import json
from beautifultable import BeautifulTable
from do_print_utils import do_print
from get_base_url import get_base_url
from konversi_tanggal_utils import konversi_tanggal
from konversi_tanggal_utils import konversi_tanggal

def print_surat_jalan_harga(doc_id, selected_printer, company_code):
    # Menggunakan get_base_url untuk mendapatkan domain yang sesuai
    base_url = get_base_url(company_code)

    # Menggunakan company_code untuk membangun URL
    response = requests.get(f"{base_url}/print/surat-jalan/{doc_id}")
    json_obj = json.loads(response.content)
    print(json_obj)

    relasi_name = json_obj['data'].get('relasi', {}).get('MASTER_RELASI_NAMA', '') if json_obj['data'].get('relasi') else ''
    supplier_name = json_obj['data'].get('supplier', {}).get('MASTER_SUPPLIER_NAMA', '') if json_obj['data'].get('supplier') else ''
    driver_name = json_obj['data'].get('driver', {}).get('MASTER_KARYAWAN_NAMA', '') if json_obj['data'].get('driver') else f'{relasi_name} {supplier_name}'

    header = BeautifulTable()
    header.columns.width = 40
    header.columns.header = [
        f"{json_obj['perusahaan']['PERUSAHAAN_NAMA']}\n"
        f"{json_obj['perusahaan']['PERUSAHAAN_ALAMAT']}\n"
        f"{json_obj['perusahaan']['PERUSAHAAN_TELP']}",
        f"Nomor: {json_obj['data']['SURAT_JALAN_NOMOR']}\n"
        f"Tanggal: {konversi_tanggal(json_obj['data']['SURAT_JALAN_TANGGAL'])}\n"
        f"Kepada: {relasi_name}{supplier_name}"
    ]
    
    header.rows.append(["", ""])
    header.set_style(BeautifulTable.STYLE_NONE)
    header.columns.alignment = BeautifulTable.ALIGN_LEFT

    table = BeautifulTable()
    table.columns.width = 20
    table.columns.header =["     Nama Barang     ", "     Harga     ","     QTY     ","     Total     "]
    grandtotal = 0
    for result in json_obj['barang']:
        total = int(result['SURAT_JALAN_BARANG_HARGA']) * int(result['SURAT_JALAN_BARANG_QUANTITY'])
        grandtotal += total
        table.rows.append([result['barangSuratJalan']['MASTER_BARANG_NAMA'], format(int(result['SURAT_JALAN_BARANG_HARGA']),',d'), result['SURAT_JALAN_BARANG_QUANTITY'],format(int(total),',d')])
    table.columns.alignment = BeautifulTable.ALIGN_RIGHT

    ttd = BeautifulTable()
    ttd.columns.width = 25
    ttd.columns.header = ["Diketahui Oleh","","Dibuat Oleh"]
    ttd.rows.append(["\n", "\n", "\n"])
    ttd.rows.append(["                         ", "                         ", "                         "])
    ttd.rows.append([f"{relasi_name} {supplier_name}".strip(), "", json_obj['user']['USER_NAMA']])
    ttd.set_style(BeautifulTable.STYLE_NONE)
    ttd.columns.alignment = BeautifulTable.ALIGN_CENTER

    judul = BeautifulTable()
    judul.columns.width = 80
    judul.columns.header = ["SURAT JALAN"]
    judul.rows.append(["                                                                      "])
    judul.set_style(BeautifulTable.STYLE_NONE)
    judul.columns.alignment = BeautifulTable.ALIGN_CENTER

    total = BeautifulTable()
    total.columns.width = 80
    total.rows.append(["","","Total (Rp)",format(int(grandtotal), ',d')])
    total.rows.append(["                     ","               ","             ","                "])
    total.set_style(BeautifulTable.STYLE_COMPACT)
    total.columns.alignment = BeautifulTable.ALIGN_RIGHT

    # with open(f'{id}.txt', 'w', encoding='utf-8') as f:
    with open(f'{doc_id}.txt', 'w') as f:
        f.write(str(header))
        f.write("\n")
        f.write(str(judul))
        f.write("\n")
        f.write(str(table))
        f.write("\n")
        f.write(str(total))
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write(str(ttd))
    do_print(doc_id,selected_printer)
