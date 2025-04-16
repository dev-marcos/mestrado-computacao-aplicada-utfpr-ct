/*============================================================================*/
/* Exemplo: segmentação de uma imagem em escala de cinza.                     */
/*----------------------------------------------------------------------------*/
/* Autor: Bogdan T. Nassu                                                     */
/* Universidade Tecnológica Federal do Paraná                                 */
/*============================================================================*/

#include <iostream>
#include <time.h>
#include <vector>
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;
using namespace cv;

/*============================================================================*/

#define INPUT_IMAGE "arroz.bmp"

// TODO: ajuste estes parâmetros!
#define NEGATIVO false
#define THRESHOLD 0.4f
#define ALTURA_MIN 1
#define LARGURA_MIN 1
#define N_PIXELS_MIN 1

/*============================================================================*/

typedef struct
{
    float label; // Rótulo do componente.
    Rect roi; // Coordenadas do retângulo envolvente do componente.
    int n_pixels; // Número de pixels do componente.

} Componente;

/*============================================================================*/

void binariza (Mat& in, Mat& out, float threshold);
void rotula (Mat& img, vector <Componente>& componentes, int largura_min, int altura_min, int n_pixels_min);

/*============================================================================*/

int main ()
{
    // Abre a imagem em escala de cinza, e mantém uma cópia colorida dela para desenhar a saída.
    Mat img = imread (INPUT_IMAGE, IMREAD_GRAYSCALE);
    if (!img.data)
    {
        cerr << "Erro abrindo a imagem.\n";
        exit (1);
    }

	// Converte para float.
	img.convertTo (img, CV_32F, 1.0/255.0);

    Mat img_out (img.rows, img.cols, CV_8UC3);
    cvtColor (img, img_out, COLOR_GRAY2BGR);

    // Segmenta a imagem.
    if (NEGATIVO)
        img = 1 - img;

    binariza (img, img, THRESHOLD);
    imshow ("01 - binarizada", img);
	imwrite ("01 - binarizada.png", img);

    vector <Componente> componentes;
    clock_t tempo_inicio = clock ();
    rotula (img, componentes, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN);
    clock_t tempo_total = clock () - tempo_inicio;

    cout << "Tempo: " << (int) tempo_total << endl;
    cout << componentes.size () << " componentes detectados" << endl;

    // Mostra os objetos encontrados.
    for (unsigned int i = 0; i < componentes.size (); i++)
        rectangle (img_out, componentes [i].roi, Scalar (0,0,1));
	imshow ("02 - out", img_out);
	imwrite ("02 - out.png", img_out);
	waitKey ();

    return (0);
}

/*----------------------------------------------------------------------------*/
/** Binarização simples por limiarização.
 *
 * Parâmetros: Mat& in: imagem de entrada. Se tiver mais que 1 canal, binariza
 *               cada canal independentemente.
 *             Mat& out: imagem de saída. Deve ter o mesmo tamanho da imagem de
 *               entrada.
 *             float threshold: limiar.
 *
 * Valor de retorno: nenhum (usa a imagem de saída). */

void binariza (Mat& in, Mat& out, float threshold)
{
    if (in.cols != out.cols || in.rows != out.rows || in.channels () != out.channels ())
    {
        cerr << "ERRO: binariza: as imagens precisam ter o mesmo tamanho e numero de canais.\n";
        exit (1);
    }

    // TODO: escreva o código desta função.
}

/*============================================================================*/
/* ROTULAGEM                                                                  */
/*============================================================================*/
/** Rotulagem usando flood fill. Marca os objetos da imagem com os valores
 * [0.1,0.2,etc].
 *
 * Parâmetros: Mat& img: imagem de entrada E saída.
 *             vector <Componente>& componentes: coloca aqui os componentes
 *               gerados.
 *             int largura_min: descarta componentes com largura menor que esta.
 *             int altura_min: descarta componentes com altura menor que esta.
 *             int n_pixels_min: descarta componentes com menos pixels que isso.
 *
 * Valor de retorno: nenhum. Usa o vetor de saída. */

void rotula (Mat& img, vector <Componente>& componentes, int largura_min, int altura_min, int n_pixels_min)
{
    // TODO: escreva esta função.
	// Use a abordagem com flood fill recursivo.
}


/*============================================================================*/
