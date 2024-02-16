using System.Drawing;
using Emgu.CV;
using Emgu.CV.Structure;
using static System.Console;

namespace Kamera_Regelung
{
    internal class CameraEvaluation
    {
        public VideoCapture vc { get; private set; }
        public MCvScalar Yellow { get; set; }
        public PointF YellowestPixel { get; private set; }

        public CameraEvaluation(VideoCapture vc)
        {
            this.vc = vc;
        }

        // search yellowest pixel in the image
        public void SearchYellowestPixel(Image<Bgr, byte> img)
        {
            Image<Hls, byte> hlsImg = img.Convert<Hls, byte>();
            int x = 0, y = 0;
            double max = 0;

            for (int i = 0; i < hlsImg.Rows; i++)
            {
                for (int j = 0; j < hlsImg.Cols; j++)
                {
                    Hls pixel = hlsImg[i, j];
                    // get h s l values
                    double h = pixel.Hue;
                    double l = pixel.Lightness;
                    double s = pixel.Satuation;
                    // check if the pixel is yellow
                    if (h > 20 && h < 40 && l > 50 && s > 50)
                    {
                        double yel = h + l + s;
                        if (yel > max)
                        {
                            max = yel;
                            x = j;
                            y = i;
                        }
                    }
                }
            }

            YellowestPixel = new PointF(x, y);
            WriteLine($"Yellowest pixel at: ({x}, {y})");
            CvInvoke.Circle(hlsImg, new Point(x, y), 5, new MCvScalar(0, 0, 255), 1);
            CvInvoke.Imwrite("yellowest_pixel.jpg", hlsImg);
        }
    }
}