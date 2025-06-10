import cv2
import numpy as np

# Trabalho 3 de PDI - Bloom
# Autor: Marcos Rocha
# Implementação própria com base nos conceitos vistos em aula.

def bright_pass(image_float, threshold):
    # RGB to Grayscale Conversion
    # https://mmuratarat.github.io/2020-05-13/rgb_to_grayscale_formulas#the-luminosity-method

    #The luminosity method
    brightness = 0.2126 * image_float[:, :, 2] + 0.7152 * image_float[:, :, 1] + 0.0722 * image_float[:, :, 0]

    # brightness = np.mean(image_float, axis=2)
    # brightness = np.max(image_float, axis=2)


    bright_pixels = brightness > (threshold / 255.0)

    mask = np.zeros_like(image_float)

    mask[bright_pixels] = image_float[bright_pixels]

    return mask

def gaussian_blur(image, sigma, iterations):

    accumulated = np.zeros_like(image)
    blurred = image.copy()

    for _ in range(iterations):
        blurred = cv2.GaussianBlur(blurred, (0, 0), sigmaX=sigma, sigmaY=sigma)
        accumulated += blurred
       
    accumulated = np.clip(accumulated, 0.0, 1.0)
    return accumulated

def box_blur_approximation(image, kernel_size, iterations):
    accumulated = np.zeros_like(image)
    blurred = image.copy()

    for _ in range(iterations):
        blurred = cv2.blur(blurred, (kernel_size, kernel_size))
        accumulated += blurred


    accumulated = np.clip(accumulated, 0.0, 1.0)
    return accumulated

def blend_images(original_float, blurred_mask, alpha, beta):
    # g(x,y) = α·f(x,y) + β·máscara(x,y)
    combined = cv2.addWeighted(original_float, alpha, blurred_mask, beta, 0.0)
    combined = np.clip(combined, 0.0, 1.0)
    return combined

def process_and_show(image_filename, method='gaussian'):
    image = cv2.imread(image_filename)
    if image is None:
        raise ValueError(f"Imagem não encontrada: {image_filename}")

    image_float = image.astype(np.float32) / 255.0

    #1. Isolando as fontes de luz
    bright = bright_pass(image_float, 135)

    #2. Borrando a máscara
    if method == 'gaussian':
        blurred = gaussian_blur(bright, sigma=10, iterations=4)
    elif method == 'box':
        blurred = box_blur_approximation(bright, kernel_size=10, iterations=4)
    else:
        raise ValueError("Método inválido. Use 'gaussian' ou 'box'.")
    
    #3. Juntando tudo
    result = blend_images(image_float, blurred, alpha=1.0, beta=0.3)

    cv2.imshow(f"Original - {image_filename}", image)
    # cv2.imshow(f"Bright Pass - {image_filename}", (bright * 255).astype(np.uint8))
    # cv2.imshow(f"Blurred - {image_filename}", (blurred * 255).astype(np.uint8))
    cv2.imshow(f"Resultado Bloom ({method}) - {image_filename}", (result * 255).astype(np.uint8))

def main():
    img1 = "GT2.BMP"
    img2 = "Wind Waker GC.bmp"

    process_and_show(img1, method='gaussian')
    process_and_show(img2, method='gaussian')
    # process_and_show(img1, method='box')
    # process_and_show(img2, method='box')

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
