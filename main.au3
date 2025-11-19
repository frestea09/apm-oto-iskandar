#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#include <MsgBoxConstants.au3>

; Membuat GUI fullscreen dengan style popup (tanpa border) untuk tampilan layar penuh
$hGUI = GUICreate("Mesin Layanan BPJS - Mudah Digunakan", @DesktopWidth, @DesktopHeight, 0, 0, $WS_POPUP)
GUISetBkColor(0xFFFFFF) ; Mengubah warna background GUI menjadi Putih
; Mengatur font yang lebih besar untuk aksesibilitas (sesuaikan jika perlu untuk layar besar)
GUISetFont(18, 400, 0, "Arial") ; Font diperbesar sedikit untuk fullscreen

; Menambahkan logo rumah sakit (ganti "logo.png" dengan path file logo Anda, pastikan file ada di direktori script atau path lengkap)
; Logo ditempatkan di kiri atas untuk visibilitas
$logo = GUICtrlCreatePic("logo.jpg", 50, 20, 150, 100) ; Ukuran logo disesuaikan, ganti path jika perlu

; Label instruksi utama (posisi disesuaikan untuk memberi ruang logo)
GUICtrlCreateLabel("Selamat datang di Mesin Layanan BPJS. Ikuti langkah-langkah berikut:", 220, 50, @DesktopWidth - 270, 60)
GUICtrlSetFont(-1, 20, 800) ; Font lebih besar

; Label untuk input Nomor BPJS
GUICtrlCreateLabel("Masukkan Nomor BPJS Anda (16 digit):", 50, 140, @DesktopWidth - 100, 40)
$inputBPJS = GUICtrlCreateInput("", 50, 190, @DesktopWidth - 100, 60) ; Input field lebih besar
GUICtrlSetTip($inputBPJS, "Masukkan nomor BPJS tanpa spasi atau tanda baca")

; Label untuk input Nomor Booking
GUICtrlCreateLabel("Masukkan Nomor Booking (jika ada):", 50, 270, @DesktopWidth - 100, 40)
$inputNomorBooking = GUICtrlCreateInput("", 50, 320, @DesktopWidth - 100, 60) ; Input field lebih besar
GUICtrlSetTip($inputNomorBooking, "Masukkan nomor booking jika Anda memiliki janji temu")

; Tombol untuk Login Frista (ukuran diperbesar untuk fullscreen)
$btnRun = GUICtrlCreateButton("1. Login dan Verifikasi Wajah (Frista)", 50, 400, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRun, 16, 800)
GUICtrlSetTip($btnRun, "Klik untuk login ke aplikasi Frista dan verifikasi wajah")

; Tombol untuk Pengisian Data BPJS
$btnRunPengisian = GUICtrlCreateButton("2. Isi Data Sidik Jari (Registrasi)", 50, 500, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRunPengisian, 16, 800)
GUICtrlSetTip($btnRunPengisian, "Klik untuk mengisi data sidik jari BPJS")

; Label instruksi tambahan
GUICtrlCreateLabel("Pastikan Anda memiliki kartu BPJS dan siap untuk verifikasi wajah atau sidik jari.", 50, 600, @DesktopWidth - 100, 50)
GUICtrlSetFont(-1, 14, 400)

; Tombol Keluar (ditempatkan di bawah)
$btnExit = GUICtrlCreateButton("Keluar", 50, 670, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnExit, 16, 800)
GUICtrlSetTip($btnExit, "Klik untuk menutup aplikasi")

; Footer: Label yang menjelaskan pembuat aplikasi
GUICtrlCreateLabel("© 2025 SIMRS RSUD Otista Soreang", 50, @DesktopHeight - 80, @DesktopWidth - 100, 40)
GUICtrlSetFont(-1, 14, 400) ; Font lebih kecil untuk footer, tapi masih mudah dibaca
GUICtrlSetColor(-1, 0x808080) ; Warna abu-abu untuk footer agar tidak terlalu mencolok

; Menampilkan GUI dalam mode fullscreen
GUISetState(@SW_SHOW)

While 1
    $nMsg = GUIGetMsg() ; Mengambil pesan dari GUI

    ; Jika tombol "Login Frista" diklik
    If $nMsg = $btnRun Then
        $bpjsNumber = GUICtrlRead($inputBPJS)
        $bookingNumber = GUICtrlRead($inputNomorBooking) ; Baca nomor booking, meskipun belum digunakan di fungsi ini

        ; Validasi input
        ;If StringLen($bpjsNumber) <> 16 Or Not StringIsDigit($bpjsNumber) Then
         ;   MsgBox($MB_ICONERROR, "Error", "Nomor BPJS harus 16 digit angka. Silakan coba lagi.")
          ;  ContinueLoop
        ;EndIf

        ; Menjalankan aplikasi Frista
        Run('"D:\BPJS\Frista\frista.exe"')
        Sleep(1000)

        ; Menunggu jendela Login Frista muncul dan aktif
        If Not WinWaitActive("Login Frista (Face Recognition BPJS Kesehatan)", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Aplikasi Frista tidak dapat dibuka. Hubungi petugas.")
            ContinueLoop
        EndIf

        $pos = WinGetPos("Login Frista (Face Recognition BPJS Kesehatan)")

        ; Mengisi username dan password
        Send("1002r006th") ; Username
        Send("{TAB}")      ; Pindah ke field password
        Send("{#}Bandung28") ; Password
        Send("{TAB}")      ; Pindah ke tombol login
        Send("{SPACE}")    ; Klik tombol login

        ; Tunggu jendela utama Frista
        If Not WinWaitActive("Frista (Face Recognition BPJS Kesehatan)", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Login gagal. Coba lagi atau hubungi petugas.")
            ContinueLoop
        EndIf

        ; Kirim nomor BPJS
        Send($bpjsNumber)
        Sleep(1000)

        ; Tunggu jendela hasil pengenalan wajah
        If Not WinWaitActive("Hasil Pengenalan Wajah", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Verifikasi wajah gagal. Pastikan wajah terlihat jelas.")
            ContinueLoop
        EndIf

        ; Klik tombol "OK"
        ControlClick("Hasil Pengenalan Wajah", "", "Button1")

        ; Tutup jendela utama Frista
        WinClose("Frista (Face Recognition BPJS Kesehatan)")

        ; Pesan sukses
        MsgBox($MB_ICONINFORMATION, "Sukses", "Verifikasi wajah selesai. Silakan lanjutkan ke langkah berikutnya.")
    EndIf

    ; Jika tombol "Pengisian Data BPJS" diklik
    If $nMsg = $btnRunPengisian Then
        $bpjsNumber = GUICtrlRead($inputBPJS)
        $bookingNumber = GUICtrlRead($inputNomorBooking)

        ; Validasi input
       ; If StringLen($bpjsNumber) <> 16 Or Not StringIsDigit($bpjsNumber) Then
        ;    MsgBox($MB_ICONERROR, "Error", "Nomor BPJS harus 16 digit angka. Silakan coba lagi.")
        ;    ContinueLoop
        ;EndIf

        ; Jalankan aplikasi After.exe
        Run('"C:\Program Files (x86)\BPJS Kesehatan\Aplikasi Sidik Jari BPJS Kesehatan\After.exe"')
        Sleep(2000)

        ; Tunggu jendela aplikasi
        If Not WinWaitActive("Aplikasi Registrasi Sidik Jari", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Aplikasi Registrasi tidak dapat dibuka. Hubungi petugas.")
            ContinueLoop
        EndIf

        ; Login
        Send("1002r006th") ; Username
        Send("{TAB}")      ; Pindah ke password
        Send("{#}Bandung28") ; Password
        Send("{TAB}")      ; Pindah ke tombol login
        Send("{ENTER}")    ; Login
		Sleep(1000)
        ; Tunggu jendela utama
        If Not WinWaitActive("Aplikasi Registrasi Sidik Jari", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Login gagal. Coba lagi atau hubungi petugas.")
            ContinueLoop
        EndIf

        ; Kirim nomor BPJS
        Send($bpjsNumber)
        Sleep(3000)

        ; Tutup aplikasi
        WinClose("Aplikasi Registrasi Sidik Jari")

        ; Pesan sukses
        MsgBox($MB_ICONINFORMATION, "Sukses", "Pengisian data sidik jari selesai. Terima kasih telah menggunakan layanan ini.")
    EndIf

    ; Jika tombol Keluar diklik
    If $nMsg = $btnExit Or $nMsg = $GUI_EVENT_CLOSE Then
        Exit
    EndIf
WEnd