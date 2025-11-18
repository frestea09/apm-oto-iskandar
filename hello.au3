; #include <MsgBoxConstants.au3>

; MsgBox($MB_OK, "Tutorial", "Hello World!")

; Run("notepad.exe")
; WinWaitActive("Untitled - Notepad")
; Send("This is some text.")
; WinWaitActive("*Untitled - Notepad")
; WinClose("*Untitled - Notepad")
; WinWaitActive("Notepad", "Save")
;WinWaitActive("Notepad", "Do you want to save") ; When running under Windows XP
;Send("{ENTER}") ; Tekan Enter untuk memilih "Don't Save" (biasanya opsi default)

#include <GUIConstantsEx.au3>  ; Menyertakan library untuk GUI

; Membuat GUI dengan ukuran 300x200 piksel
;$hGUI = GUICreate("Contoh GUI dengan Dua Tombol", 400, 300)

; Membuat tombol pertama dengan teks "Tombol 1"
;$btn1 = GUICtrlCreateButton("Tombol 1", 50, 50, 80, 30)

; Membuat tombol kedua dengan teks "Tombol 2"
;$btn2 = GUICtrlCreateButton("Tombol 2", 150, 50, 80, 30)
; Membuat GUI dan tombol-tombol
$hGUI = GUICreate("Contoh GUI", 500, 300)

; Tombol untuk menjalankan aplikasi Frista
$btnRun = GUICtrlCreateButton("Login Frista", 50, 50, 400, 30)

; Tombol untuk melakukan pengisian (sama seperti tombol pertama untuk contoh)
$btnRunPengisian = GUICtrlCreateButton("Pengisian Data BPJS", 50, 100, 400, 30)
$inputBPJS = GUICtrlCreateInput("", 50, 150, 400, 30)  ; Kolom input untuk BPJS
; Menampilkan GUI
GUISetState()

While 1
    $nMsg = GUIGetMsg()  ; Mengambil pesan dari GUI

    ; Jika tombol "Jalankan Aplikasi Frista" diklik
    If $nMsg = $btnRun Then
		$bpjsNumber = GUICtrlRead($inputBPJS)
        ; Menjalankan aplikasi Frista
         Run('"D:\BPJS\Frista\frista.exe"')

        ; Menunggu jendela Login Frista muncul dan aktif
        WinWaitActive("Login Frista (Face Recognition BPJS Kesehatan)")
		$pos = WinGetPos("Login Frista (Face Recognition BPJS Kesehatan)")
        ; Mengisi username dan password
        Send("1002r006th")  ; Username
        Send("{TAB}")       ; Pindah ke field password
        Send("{#}Bandung28") ; Password
        Send("{TAB}")     ; Tekan Enter untuk login
		Send("{SPACE}")
		$x = $pos[0] + $pos[2] / 2 ; Koordinat X tengah
        $y = $pos[1] + $pos[3] / 2 ; Koordinat Y tengah

        ; Mengklik di tengah jendela
        MouseClick("left", $x, $y)
		WinWaitActive("Frista (Face Recognition BPJS Kesehatan)")
		Send($bpjsNumber)
		WinWaitActive("Hasil Pengenalan Wajah")

		; Klik tombol "OK" di jendela "Hasil Pengenalan Wajah"
		ControlClick("Hasil Pengenalan Wajah", "", "Button1")  ; Mengklik tombol OK

		; Meminimalkan jendela utama Frista (Face Recognition BPJS Kesehatan)
		WinClose("Frista (Face Recognition BPJS Kesehatan)")

    EndIf

    ; Jika tombol "Pengisian Data BPJS" diklik
    If $nMsg = $btnRunPengisian Then
		Run('"C:\Program Files (x86)\BPJS Kesehatan\Aplikasi Sidik Jari BPJS Kesehatan\After.exe"')
		Sleep(2500)
		WinWaitActive("Aplikasi Registrasi Sidik Jari")
		Send("1002r006th")  ; Username
        Send("{TAB}")       ; Pindah ke field password
        Send("{#}Bandung28") ; Password
        Send("{TAB}")     ; Tekan Enter untuk login
		Send("{ENTER}")
		Sleep(2500)
		WinWaitActive("Aplikasi Registrasi Sidik Jari")
		Send("0000053468649")
		Sleep(3000)
		WinClose("Aplikasi Registrasi Sidik Jari")

    EndIf

    ; Jika pengguna menutup jendela GUI
    If $nMsg = $GUI_EVENT_CLOSE Then
        Exit
    EndIf
WEnd