# Smooth Gear Generator

**SmoothGearGenerator** is a Fusion 360 script designed to generate simplified, smooth gear profiles, making it ideal for basic 3D printing applications. This script maximizes ease of use and reliably generates simple gear profiles with curved geometry, minimizing wear surfaces and reducing the need for high printing acceleration in FDM applications.

You can also test it out interactively at: [Desmos Smooth Gear Sim](https://www.desmos.com/calculator/fffw2eqnt1)

## Installation

1. Download the script file [SmoothGearGenerator.py](#link-to-file).
2. Open **Autodesk Fusion 360**.
3. Navigate to the `Scripts and Add-Ins` panel under the `Utilities` tab.
4. Next to `My Scripts`, press the green `+`.
5. Browse to the location of `SmoothGearGenerator.py` and press `Open`.

## Usage

1. Select the script from the `Scripts and Add-Ins` menu in Fusion 360 and click `▶Run`
3. A user interface will appear, allowing you to customize gear parameters such as the module and the number of teeth.
4. Adjust the parameters as needed and click `OK` to generate the profile.

*Note:* This script has been tested with Fusion 360 version 2.0.19994, but it should be compatible with other recent versions as well.

### Parameters

- **Module (m)**: Determines the size of the gear. Intersecting gears need to have the same module. The pitch diameter is calculated as `Module × Number of Teeth`.
- **Number of Teeth (z)**: Defines how many teeth the gear will have. More teeth result in a larger gear with finer details.

## Configuration

You can configure additional settings at the top of the script file:

- **`pointsPerTooth`**: The number of vertices per tooth. Higher values increase detail but may cause lag, especially with more complex gears. Ideal for high-resolution printing.
- **`rounding`**: Adjusts the roundness of the gear profile (values between `0.0` to `1.0`). This option influences the aesthetics by making the profile closer to a circle, but be aware that higher values may reduce performance.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributions

Feel free to submit pull requests or open issues for any bugs or feature requests.
