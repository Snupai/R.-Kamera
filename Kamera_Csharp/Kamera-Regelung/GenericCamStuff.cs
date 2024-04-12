using static System.Console;
using Emgu.CV;
using DirectShowLib;
using System.Diagnostics;

namespace Kamera_Regelung
{
    internal class GenericCamStuff
    {
        public VideoCapture vc { get; private set; }
        public string cameraName { get; private set; }
        public double frameRate { get; private set; }
        public double frameWidth { get; private set; }
        public double frameHeight { get; private set; }
        public double brightness { get; private set; }
        public double contrast { get; private set; }
        public double saturation { get; private set; }
        public double hue { get; private set; }
        public double gain { get; private set; }
        public double exposure { get; private set; }
        public double whiteBalance { get; private set; }
        public double sharpness { get; private set; }
        public double gamma { get; private set; }
        public double temperature { get; private set; }
        public double zoom { get; private set; }
        public double focus { get; private set; }
        public double iris { get; private set; }
        public double pan { get; private set; }
        public double tilt { get; private set; }
        public double roll { get; private set; }

        public GenericCamStuff(VideoCapture vc, string cameraName)
        {
            this.vc = vc;
            this.cameraName = cameraName;
            frameRate = vc.Get(Emgu.CV.CvEnum.CapProp.Fps);
            frameWidth = vc.Get(Emgu.CV.CvEnum.CapProp.FrameWidth);
            frameHeight = vc.Get(Emgu.CV.CvEnum.CapProp.FrameHeight);
            brightness = vc.Get(Emgu.CV.CvEnum.CapProp.Brightness);
            contrast = vc.Get(Emgu.CV.CvEnum.CapProp.Contrast);
            saturation = vc.Get(Emgu.CV.CvEnum.CapProp.Saturation);
            hue = vc.Get(Emgu.CV.CvEnum.CapProp.Hue);
            gain = vc.Get(Emgu.CV.CvEnum.CapProp.Gain);
            exposure = vc.Get(Emgu.CV.CvEnum.CapProp.Exposure);
            whiteBalance = vc.Get(Emgu.CV.CvEnum.CapProp.WhiteBalanceBlueU);
            sharpness = vc.Get(Emgu.CV.CvEnum.CapProp.Sharpness);
            gamma = vc.Get(Emgu.CV.CvEnum.CapProp.Gamma);
            temperature = vc.Get(Emgu.CV.CvEnum.CapProp.Temperature);
            zoom = vc.Get(Emgu.CV.CvEnum.CapProp.Zoom);
            focus = vc.Get(Emgu.CV.CvEnum.CapProp.Focus);
            iris = vc.Get(Emgu.CV.CvEnum.CapProp.Iris);
            pan = vc.Get(Emgu.CV.CvEnum.CapProp.Pan);
            tilt = vc.Get(Emgu.CV.CvEnum.CapProp.Tilt);
            roll = vc.Get(Emgu.CV.CvEnum.CapProp.Roll);
        }

        /// <summary>
        /// Gibt eine Liste aller verfügbaren Kameras zurück.
        /// </summary>
        /// <returns></returns>
        internal static List<DsDevice> GetCameras()
        {
            var devices = new List<DsDevice>();
            devices.AddRange(DsDevice.GetDevicesOfCat(FilterCategory.VideoInputDevice));
            foreach (var device in devices)
            {
                WriteLine($"ID: {devices.IndexOf(device)} | Name: {device.Name}");
            }
            return devices;
        }

        /// <summary>
        /// Öffnet den Kamerastream und zeigt das Bild in einem Fenster an.
        /// </summary>
        /// <param name="vc"></param>
        internal void OpenCameraStream(VideoCapture vc)
        {
            // Starte die Kamera
            vc.Start();

            Stopwatch sw = new Stopwatch();

            while (true)
            {
                sw.Start();
                // Lese das aktuelle Bild der Kamera
                Mat frame = vc.QueryFrame();

                // Zeige das Bild in einem Fenster
                CvInvoke.Imshow("Kamera", frame);

                // Warte auf Benutzereingabe
                if ((CvInvoke.WaitKey(1) & 0xFF) == 0x1B || (CvInvoke.WaitKey(1) & 0xFF) == 0x71)
                {
                    CvInvoke.DestroyAllWindows();
                    break;
                }
                sw.Stop();
                WriteLine($"Zeit: {sw.ElapsedMilliseconds} ms");
                sw.Reset();
            }

            // Stoppe die Kamera
            vc.Stop();
        }

        /// <summary>
        /// Gibt die Eigenschaften der Kamera aus.
        /// </summary>
        /// <param name="vc"></param>
        internal void GetDeviceInfo(VideoCapture vc)
        {
            // Ausgabe der Kameraeigenschaften
            WriteLine($"Kamera: {cameraName}");
            WriteLine($"Bildrate: {frameRate} fps");
            WriteLine($"Auflösung: {frameWidth}x{frameHeight}");
            WriteLine($"Helligkeit: {brightness}");
            WriteLine($"Kontrast: {contrast}");
            WriteLine($"Sättigung: {saturation}");
            WriteLine($"Farbton: {hue}");
            WriteLine($"Verstärkung: {gain}");
            WriteLine($"Belichtung: {exposure}");
            WriteLine($"Weißabgleich: {whiteBalance}");
            WriteLine($"Schärfe: {sharpness}");
            WriteLine($"Gamma: {gamma}");
            WriteLine($"Temperatur: {temperature}");
            WriteLine($"Zoom: {zoom}");
            WriteLine($"Fokus: {focus}");
            WriteLine($"Iris: {iris}");
            WriteLine($"Pan: {pan}");
            WriteLine($"Tilt: {tilt}");
            WriteLine($"Roll: {roll}");
        }
    }
}