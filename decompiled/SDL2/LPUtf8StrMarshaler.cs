using System;
using System.Runtime.InteropServices;
using System.Text;

namespace SDL2;

internal class LPUtf8StrMarshaler : ICustomMarshaler
{
	public const string LeaveAllocated = "LeaveAllocated";

	private static ICustomMarshaler _leaveAllocatedInstance = new LPUtf8StrMarshaler(leaveAllocated: true);

	private static ICustomMarshaler _defaultInstance = new LPUtf8StrMarshaler(leaveAllocated: false);

	private bool _leaveAllocated;

	public LPUtf8StrMarshaler(bool leaveAllocated)
	{
		_leaveAllocated = leaveAllocated;
	}

	public static ICustomMarshaler GetInstance(string cookie)
	{
		if (cookie == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831529))
		{
			return _leaveAllocatedInstance;
		}
		return _defaultInstance;
	}

	public unsafe object MarshalNativeToManaged(IntPtr pNativeData)
	{
		if (pNativeData == IntPtr.Zero)
		{
			return null;
		}
		byte* ptr;
		for (ptr = (byte*)(void*)pNativeData; *ptr != 0; ptr++)
		{
		}
		byte[] array = new byte[ptr - (byte*)(void*)pNativeData];
		Marshal.Copy(pNativeData, array, 0, array.Length);
		return Encoding.UTF8.GetString(array);
	}

	public unsafe IntPtr MarshalManagedToNative(object ManagedObj)
	{
		if (ManagedObj == null)
		{
			return IntPtr.Zero;
		}
		if (!(ManagedObj is string s))
		{
			throw new ArgumentException(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831444), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831473));
		}
		byte[] bytes = Encoding.UTF8.GetBytes(s);
		IntPtr intPtr = SDL.SDL_malloc((IntPtr)(bytes.Length + 1));
		Marshal.Copy(bytes, 0, intPtr, bytes.Length);
		((sbyte*)(void*)intPtr)[bytes.Length] = 0;
		return intPtr;
	}

	public void CleanUpManagedData(object ManagedObj)
	{
	}

	public void CleanUpNativeData(IntPtr pNativeData)
	{
		if (!_leaveAllocated)
		{
			SDL.SDL_free(pNativeData);
		}
	}

	public int GetNativeDataSize()
	{
		return -1;
	}
}
