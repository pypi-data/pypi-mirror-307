#include "no_lch.h"

bool no_lch::is_lch_possible(Point* /* leader */, Point* /* follower */, Point* /* new_leader */, Point* /* new_follower */, Model* /* cfpars */, params* /* lcmpars */)
{
    return false;
}

no_lch::no_lch()
{
	_cf = nullptr;
	_lcpars = nullptr;
}

bool no_lch::lch_left(Point* /* leader */, Point* /* follower */, Point* /* new_leader */, Point* /* new_follower */, Model* /* cfpars */, params* /* lcmpars */)
{
    return false;
}

bool no_lch::lch_right(Point* /* leader */, Point* /* follower */, Point* /* new_leader */, Point* /* new_follower */, Model* /* cfpars */, params* /* lcmpars */)
{
    return false;
}
