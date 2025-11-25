#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#include <MsgBoxConstants.au3>

Global $fristaPath = 'frista.exe'
Global $afterPath = 'C:\Program Files (x86)\BPJS Kesehatan\Aplikasi Sidik Jari BPJS Kesehatan\After.exe'

; Cek jika file settings.ini ada, jika ada, load path dari file tersebut
If FileExists('settings.ini') Then
    $fristaPath = IniRead('settings.ini', 'Paths', 'Frista', $fristaPath)
    $afterPath = IniRead('settings.ini', 'Paths', 'After', $afterPath)
EndIf


; Membuat GUI fullscreen dengan style popup (tanpa border) untuk tampilan layar penuh
$hGUI = GUICreate("Mesin Layanan BPJS - Mudah Digunakan", @DesktopWidth, @DesktopHeight, 0, 0, $WS_POPUP)
GUISetBkColor(0xFFFFFF) ; Mengubah warna background GUI menjadi Putih
; Mengatur font yang lebih besar untuk aksesibilitas (sesuaikan jika perlu untuk layar besar)
GUISetFont(18, 400, 0, "Arial") ; Font diperbesar sedikit untuk fullscreen

; Menambahkan menu bar
$menuBar = GUICtrlCreateMenu("Menu")
$menuApp = GUICtrlCreateMenuItem("Buka Aplikasi", $menuBar)
$menuSettings = GUICtrlCreateMenuItem("Pengaturan Aplikasi", $menuBar)

; Menambahkan logo rumah sakit (ganti "logo.png" dengan path file logo Anda, pastikan file ada di direktori script atau path lengkap)
; Logo ditempatkan di kiri atas untuk visibilitas
$logo = GUICtrlCreatePic("logo.jpg", 50, 20, 150, 100) ; Ukuran logo disesuaikan, ganti path jika perlu

; Label instruksi utama (posisi disesuaikan untuk memberi ruang logo)
GUICtrlCreateLabel("Selamat datang di Mesin Layanan BPJS. Ikuti langkah-langkah berikut:", 220, 50, @DesktopWidth - 270, 60)
GUICtrlSetFont(-1, 20, 800) ; Font lebih besar

; Label untuk input Nomor BPJS
GUICtrlCreateLabel("Masukkan Nomor BPJS Anda :", 50, 140, @DesktopWidth - 100, 40)
$inputBPJS = GUICtrlCreateInput("", 50, 190, @DesktopWidth - 100, 60) ; Input field lebih besar
GUICtrlSetTip($inputBPJS, "Masukkan nomor BPJS tanpa spasi atau tanda baca")

; Label untuk input Nomor Booking
;GUICtrlCreateLabel("Masukkan Nomor Booking (jika ada):", 50, 270, @DesktopWidth - 100, 40)
;$inputNomorBooking = GUICtrlCreateInput("", 50, 320, @DesktopWidth - 100, 60) ; Input field lebih besar
;GUICtrlSetTip($inputNomorBooking, "Masukkan nomor booking jika Anda memiliki janji temu")

; Tombol untuk Login Frista (ukuran diperbesar untuk fullscreen)
$btnRun = GUICtrlCreateButton("Login dan Verifikasi Wajah (Frista)", 50, 400, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRun, 16, 800)
GUICtrlSetTip($btnRun, "Klik untuk login ke aplikasi Frista dan verifikasi wajah")

; Tombol untuk Pengisian Data BPJS
$btnRunPengisian = GUICtrlCreateButton("Isi Data Sidik Jari (Registrasi)", 50, 500, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRunPengisian, 16, 800)
GUICtrlSetTip($btnRunPengisian, "Klik untuk mengisi data sidik jari BPJS")

; Tombol untuk
$btnRunTiket = GUICtrlCreateButton("Print Tiket", 50, 600, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRunTiket, 16, 800)

; Label instruksi tambahan
GUICtrlCreateLabel("Pastikan Anda memiliki kartu BPJS dan siap untuk verifikasi wajah atau sidik jari.", 50, 700, @DesktopWidth - 100, 50)
GUICtrlSetFont(-1, 14, 400)

; Tombol Keluar (ditempatkan di bawah)
$btnExit = GUICtrlCreateButton("Keluar", 50, 750, @DesktopWidth - 100, 60)
GUICtrlSetFont($btnExit, 16, 800)
GUICtrlSetTip($btnExit, "Klik untuk menutup aplikasi")

; Footer: Label yang menjelaskan pembuat aplikasi
GUICtrlCreateLabel("© 2025 SIMRS RSUD Otista Soreang", 50, 820, @DesktopWidth - 100, 40)
GUICtrlSetFont(-1, 14, 400) ; Font lebih kecil untuk footer, tapi masih mudah dibaca
GUICtrlSetColor(-1, 0x808080) ; Warna abu-abu untuk footer agar tidak terlalu mencolok

; Menampilkan GUI dalam mode fullscreen
GUISetState(@SW_SHOW)


While 1
    $nMsg = GUIGetMsg() ; Mengambil pesan dari GUI
	 If $nMsg = $menuApp Then
       Run($fristaPath) ; Jalankan aplikasi Frista
    EndIf

    ; Jika item menu "Pengaturan Aplikasi" diklik
    If $nMsg = $menuSettings Then
        OpenSettingsMenu()  ; Buka menu pengaturan untuk memilih path aplikasi
    EndIf
    ; Jika tombol "Login Frista" diklik
    If $nMsg = $btnRun Then
        $bpjsNumber = GUICtrlRead($inputBPJS)
        ;$bookingNumber = GUICtrlRead($inputNomorBooking) ; Baca nomor booking, meskipun belum digunakan di fungsi ini

        ; Validasi input
        ;If StringLen($bpjsNumber) <> 16 Or Not StringIsDigit($bpjsNumber) Then
         ;   MsgBox($MB_ICONERROR, "Error", "Nomor BPJS harus 16 digit angka. Silakan coba lagi.")
          ;  ContinueLoop
        ;EndIf

        ; Menjalankan aplikasi Frista
        Run($fristaPath)
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
        ;$bookingNumber = GUICtrlRead($inputNomorBooking)

        ; Validasi input
       ; If StringLen($bpjsNumber) <> 16 Or Not StringIsDigit($bpjsNumber) Then
        ;    MsgBox($MB_ICONERROR, "Error", "Nomor BPJS harus 16 digit angka. Silakan coba lagi.")
        ;    ContinueLoop
        ;EndIf

        ; Jalankan aplikasi After.exe
        Run($afterPath)
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
        Sleep(4000)

        ; Tutup aplikasi
        WinClose("Aplikasi Registrasi Sidik Jari")

        ; Pesan sukses
        MsgBox($MB_ICONINFORMATION, "Sukses", "Pengisian data sidik jari selesai. Terima kasih telah menggunakan layanan ini.")

		GUICtrlSetData($inputBPJS, "")  ; Mengosongkan input BPJS agar siap dibaca ulang

    EndIf
	If $nMsg = $btnRunTiket Then
		; Membuka URL di Google Chrome
		Run('C:\Program Files\Google\Chrome\Application\chrome.exe http://172.168.1.175:8070')
		Sleep(3000)  ; Tunggu beberapa detik untuk memastikan halaman terbuka

		; Menunggu jendela dengan judul "PENDAFTARAN ONLINE : RSUD OTISTA BANDUNG" aktif
		WinWaitActive("PENDAFTARAN ONLINE : RSUD OTISTA BANDUNG - Google Chrome", "", 10)

		; Klik tombol pendaftaran online (menggunakan koordinat yang diberikan)
		;MouseClick("left", 773, 209)  ; Koordinat untuk klik pada tombol pendaftaran
		Sleep(2000)  ; Tunggu beberapa detik agar proses pendaftaran selesai

		; Setelah proses pendaftaran selesai, menunggu jendela "Cetak Resume Pendaftaran Online"
		WinWaitActive("Cetak Resume Pendaftaran Online - Google Chrome", "", 10)

		; Tekan Ctrl + P untuk membuka dialog cetak
		;Send("^p")
		Sleep(3000)  ; Tunggu beberapa detik agar dialog cetak muncul

		; Klik tombol Print di dialog (menggunakan koordinat yang diberikan)
		;MouseClick("left", 373, 332)  ; Koordinat untuk klik tombol Print
		Sleep(2000)  ; Tunggu beberapa detik agar proses print selesai
		WinClose("PENDAFTARAN ONLINE : RSUD OTISTA BANDUNG - Google Chrome")
		; Kembali ke aplikasi (opsional, jika perlu)
		; WinActivate("Frista (Face Recognition BPJS Kesehatan)")  ; Jika Anda perlu kembali ke aplikasi lain
		MsgBox($MB_ICONINFORMATION, "Sukses", "Verifikasi wajah selesai. Silakan lanjutkan ke langkah berikutnya.")
		; Membuka jendela Mesin Layanan BPJS
		;Run('C:\Path\to\BPJS_Layanan.exe')  ; Ganti dengan path yang sesuai ke aplikasi Mesin Layanan BPJS
		;Sleep(2000)  ; Tunggu beberapa detik untuk memastikan aplikasi terbuka

		; Menunggu jendela dengan judul "Mesin Layanan BPJS - Mudah Digunakan" muncul
		WinWait("Mesin Layanan BPJS - Mudah Digunakan", "", 10)

		; Menempatkan jendela pada posisi yang diinginkan (misalnya posisi kiri atas layar)
		WinMove("Mesin Layanan BPJS - Mudah Digunakan", "", 0, 0)  ; Menempatkan jendela di posisi (0, 0)

		; Meminimalkan jendela tersebut
		WinSetState("Mesin Layanan BPJS - Mudah Digunakan", "", @SW_MINIMIZE)  ; Meminimalkan jendela

		; Memberikan waktu beberapa detik untuk meminimalkan jendela
		Sleep(2000)

		; Menampilkan kembali jendela yang telah diminimalkan
		WinActivate("Mesin Layanan BPJS - Mudah Digunakan")  ; Mengaktifkan kembali jendela tersebut
	EndIf
    ; Jika tombol Keluar diklik
    If $nMsg = $btnExit Or $nMsg = $GUI_EVENT_CLOSE Then
        Exit
    EndIf
WEnd

 Fungsi untuk membuka menu pengaturan aplikasi
Func OpenSettingsMenu()
    $settingsGUI = GUICreate("Pengaturan Aplikasi", 400, 300)
    GUISetFont(12)

    ; Menampilkan path aplikasi Frista dan After
    GUICtrlCreateLabel("Frista Path:", 10, 10, 150, 30)
    $txtFristaPath = GUICtrlCreateInput($fristaPath, 150, 10, 200, 30)

    GUICtrlCreateLabel("After Path:", 10, 50, 150, 30)
    $txtAfterPath = GUICtrlCreateInput($afterPath, 150, 50, 200, 30)

    ; Tombol Browse untuk memilih file aplikasi
    $btnBrowseFrista = GUICtrlCreateButton("Browse", 360, 10, 30, 30)
    $btnBrowseAfter = GUICtrlCreateButton("Browse", 360, 50, 30, 30)

    ; Tombol Simpan dan Batal
    $btnSave = GUICtrlCreateButton("Simpan", 50, 200, 100, 40)
    $btnCancel = GUICtrlCreateButton("Batal", 250, 200, 100, 40)

    GUISetState(@SW_SHOW)

    ; Event loop untuk pengaturan
    While 1
        $msg = GUIGetMsg()

        If $msg = $btnCancel Or $msg = $GUI_EVENT_CLOSE Then
            GUIDelete($settingsGUI)
            Return
        EndIf

        If $msg = $btnSave Then
            $newFristaPath = GUICtrlRead($txtFristaPath)
            $newAfterPath = GUICtrlRead($txtAfterPath)

            ; Simpan path baru ke file settings.ini
            IniWrite('settings.ini', 'Paths', 'Frista', $newFristaPath)
            IniWrite('settings.ini', 'Paths', 'After', $newAfterPath)

            ; Update path aplikasi global
            $fristaPath = $newFristaPath
            $afterPath = $newAfterPath

            MsgBox($MB_ICONINFORMATION, "Sukses", "Pengaturan disimpan.")
            GUIDelete($settingsGUI)
            Return
        EndIf

        ; Fitur Browse untuk memilih file path aplikasi
        If $msg = $btnBrowseFrista Then
            $filePath = FileOpenDialog("Pilih Aplikasi Frista", "", "Executable Files (*.exe)", 1)
            If @error = 0 Then
                GUICtrlSetData($txtFristaPath, $filePath)
            EndIf
        EndIf

        If $msg = $btnBrowseAfter Then
            $filePath = FileOpenDialog("Pilih Aplikasi After", "", "Executable Files (*.exe)", 1)
            If @error = 0 Then
                GUICtrlSetData($txtAfterPath, $filePath)
            EndIf
        EndIf
    WEnd
EndFunc