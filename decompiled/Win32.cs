using System.Runtime.InteropServices;
using System.Text;

public static class Win32
{
	[DllImport("user32.dll")]
	public static extern long GetKeyboardLayoutName(StringBuilder pwszKLID);
}
