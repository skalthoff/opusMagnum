public sealed class ChapterUnlockEvent : _0023_003Dq4_mB4SrrjjAYQr5ea7dt9Q_003D_003D
{
	public readonly CampaignChapter _0023_003DqhLrEh61I5_T5A8nImIJQWw_003D_003D;

	public ChapterUnlockEvent(CampaignChapter _0023_003Dq95TqKdF9JPo6Z4VvzBtWvQ_003D_003D)
	{
		_0023_003DqhLrEh61I5_T5A8nImIJQWw_003D_003D = _0023_003Dq95TqKdF9JPo6Z4VvzBtWvQ_003D_003D;
	}

	public override bool Equals(object _0023_003DqMswFfBkR9lbImJGwL5lcBw_003D_003D)
	{
		if (_0023_003DqMswFfBkR9lbImJGwL5lcBw_003D_003D is ChapterUnlockEvent chapterUnlockEvent)
		{
			return chapterUnlockEvent._0023_003DqhLrEh61I5_T5A8nImIJQWw_003D_003D == _0023_003DqhLrEh61I5_T5A8nImIJQWw_003D_003D;
		}
		return false;
	}

	public override int GetHashCode()
	{
		return _0023_003DqhLrEh61I5_T5A8nImIJQWw_003D_003D.GetHashCode();
	}
}
