import argparse

from .processor import DataProcessor

def main():
    parser = argparse.ArgumentParser(description="Process DICOM paths and save the results.")
    parser.add_argument('-Patient_Identifier', type=int, required=True, help="Patient Identifier (e.g., 123456)")
    parser.add_argument('-dicom_path_T0', type=str, required=True, help="Path to the T0 DICOM series directory")
    parser.add_argument('-dicom_path_T1', type=str, required=True, help="Path to the T1 DICOM series directory")
    parser.add_argument('-time_interval', type=int, required=True, help="Time interval between scans in days")
    parser.add_argument('-save_file', type=str, required=True, help="Path to save the output file")
    parser.add_argument('-verbose', type=int, default=0, help="Verbosity level (0 for silent, higher for more output)")

    args = parser.parse_args()

    DataProcessor(
        Patient_Identifier=args.Patient_Identifier,
        dicom_path_T0=args.dicom_path_T0,
        dicom_path_T1=args.dicom_path_T1,
        time_interval=args.time_interval,
        save_file=args.save_file,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()