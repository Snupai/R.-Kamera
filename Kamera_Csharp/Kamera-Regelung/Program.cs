using static System.Console;
using Emgu.CV;
using DirectShowLib;
using static Kamera_Regelung.GenericCamStuff;
using Emgu.CV.Structure;
using System.Device.Gpio; // for future GPIO pin control

namespace Kamera_Regelung
{
    class Program
    {
        static void Main(string[] args)
        {
            Int16 camID;
            List<DsDevice> devices = GetCameras();
            if (devices.Count == 0)
            {
                WriteLine("Keine Kamera gefunden.");
                return;
            }

            Write("\nBitte wählen Sie die Kamera aus, die Sie verwenden möchten (ID eingeben): ");
            try
            {
                camID = Convert.ToInt16(ReadLine());
                if (camID < 0 || camID >= devices.Count)
                {
                    throw new Exception("ID out of range");
                }
            }
            catch (Exception e)
            {
                WriteLine($"Fehler: {e.Message}");
                return;
            }
            // Erstelle eine neue Instanz der Klasse Kamera
            VideoCapture vc = new VideoCapture(camID);
            GenericCamStuff gcs = new GenericCamStuff(vc, devices[camID].Name);
            // Zeige die Eigenschaften der Kamera
            gcs.GetDeviceInfo(vc);

            // Nutzerabfrage Kamerastream öffnen
            Write("\nMöchten Sie den Kamerastream öffnen? (j/N): ");
            string input = ReadLine();
            if (input.ToLower() == "j")
            {
                // Öffne den Kamerastream
                gcs.OpenCameraStream(vc);
                return;
            }

            // Nutzerabfrage gelbsten Pixel suchen
            Write("\nMöchten Sie den gelbsten Pixel suchen? (j/N): ");
            input = ReadLine();
            if (input.ToLower() == "j")
            {
                // user input Image file
                Write("\nBitte geben Sie den Pfad zum Bild an: ");
                string path = ReadLine();
                Image<Bgr, byte> img = CvInvoke.Imread(path).ToImage<Bgr, byte>();
                CameraEvaluation ce = new CameraEvaluation(vc);
                ce.SearchYellowestPixel(img);
                return;
            }
        }
    }
}
