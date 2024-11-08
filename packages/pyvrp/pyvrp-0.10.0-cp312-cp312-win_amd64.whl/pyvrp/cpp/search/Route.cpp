#include "Route.h"

#include <cmath>
#include <numbers>
#include <ostream>
#include <utility>

using pyvrp::search::Route;

Route::Node::Node(size_t loc) : loc_(loc), idx_(0), route_(nullptr) {}

Route::Route(ProblemData const &data, size_t idx, size_t vehicleType)
    : data(data),
      vehicleType_(data.vehicleType(vehicleType)),
      vehTypeIdx_(vehicleType),
      idx_(idx),
      startDepot_(vehicleType_.startDepot),
      endDepot_(vehicleType_.endDepot)
{
    clear();
}

Route::~Route() { clear(); }

std::vector<Route::Node *>::const_iterator Route::begin() const
{
    return nodes.begin() + 1;
}
std::vector<Route::Node *>::const_iterator Route::end() const
{
    return nodes.end() - 1;
}

std::vector<Route::Node *>::iterator Route::begin()
{
    return nodes.begin() + 1;
}
std::vector<Route::Node *>::iterator Route::end() { return nodes.end() - 1; }

std::pair<double, double> const &Route::centroid() const
{
    assert(!dirty);
    return centroid_;
}

size_t Route::vehicleType() const { return vehTypeIdx_; }

bool Route::overlapsWith(Route const &other, double tolerance) const
{
    assert(!dirty && !other.dirty);

    auto const [dataX, dataY] = data.centroid();
    auto const [thisX, thisY] = centroid_;
    auto const [otherX, otherY] = other.centroid_;

    // Each angle is in [-pi, pi], so the absolute difference is in [0, tau].
    auto const thisAngle = std::atan2(thisY - dataY, thisX - dataX);
    auto const otherAngle = std::atan2(otherY - dataY, otherX - dataX);
    auto const absDiff = std::abs(thisAngle - otherAngle);

    // First case is obvious. Second case exists because tau and 0 are also
    // close together but separated by one period.
    auto constexpr tau = 2 * std::numbers::pi;
    return absDiff <= tolerance * tau || absDiff >= (1 - tolerance) * tau;
}

void Route::clear()
{
    for (auto *node : nodes)  // unassign all nodes from route.
    {
        node->idx_ = 0;
        node->route_ = nullptr;
    }

    nodes.clear();  // clear nodes and reinsert the depots.
    nodes.push_back(&startDepot_);
    nodes.push_back(&endDepot_);

    startDepot_.idx_ = 0;
    startDepot_.route_ = this;

    endDepot_.idx_ = 1;
    endDepot_.route_ = this;

    // Clear all existing statistics and reinsert depot statistics.
    distAt = {DistanceSegment(vehicleType_.startDepot),
              DistanceSegment(vehicleType_.endDepot)};
    distAfter = distAt;
    distBefore = distAt;

    LoadSegments depotLoad = {LoadSegment(0, 0, 0), LoadSegment(0, 0, 0)};
    loadAt = std::vector<LoadSegments>(data.numLoadDimensions(), depotLoad);
    loadAfter = loadAt;
    loadBefore = loadAt;

    load_ = std::vector<Load>(data.numLoadDimensions(), 0);
    excessLoad_ = load_;

    durAt = {DurationSegment(vehicleType_.startDepot, vehicleType_),
             DurationSegment(vehicleType_.endDepot, vehicleType_)};
    durAfter = durAt;
    durBefore = durAt;

#ifndef NDEBUG
    dirty = false;
#endif
}

void Route::insert(size_t idx, Node *node)
{
    assert(0 < idx && idx < nodes.size());
    assert(!node->route());  // must previously have been unassigned

    node->idx_ = idx;
    node->route_ = this;
    nodes.insert(nodes.begin() + idx, node);

    for (size_t after = idx; after != nodes.size(); ++after)
        nodes[after]->idx_ = after;

    // We do not need to update the statistics; Route::update() will handle
    // that later. We just need to ensure the right client data is inserted.
    distAt.emplace(distAt.begin() + idx, node->client());
    distBefore.emplace(distBefore.begin() + idx, node->client());
    distAfter.emplace(distAfter.begin() + idx, node->client());

    ProblemData::Client const &client = data.location(node->client());

    for (size_t dim = 0; dim != data.numLoadDimensions(); ++dim)
    {
        auto const clientLs = LoadSegment(client, dim);
        loadAt[dim].insert(loadAt[dim].begin() + idx, clientLs);
        loadAfter[dim].insert(loadAfter[dim].begin() + idx, clientLs);
        loadBefore[dim].insert(loadBefore[dim].begin() + idx, clientLs);
    }

    durAt.emplace(durAt.begin() + idx, node->client(), client);
    durAfter.emplace(durAfter.begin() + idx, node->client(), client);
    durBefore.emplace(durBefore.begin() + idx, node->client(), client);

#ifndef NDEBUG
    dirty = true;
#endif
}

void Route::push_back(Node *node)
{
    insert(size() + 1, node);

#ifndef NDEBUG
    dirty = true;
#endif
}

void Route::remove(size_t idx)
{
    assert(0 < idx && idx < nodes.size() - 1);
    assert(nodes[idx]->route() == this);  // must currently be in this route

    auto *node = nodes[idx];

    node->idx_ = 0;
    node->route_ = nullptr;

    nodes.erase(nodes.begin() + idx);

    for (auto after = idx; after != nodes.size(); ++after)
        nodes[after]->idx_ = after;

    distAt.erase(distAt.begin() + idx);
    distBefore.erase(distBefore.begin() + idx);
    distAfter.erase(distAfter.begin() + idx);

    for (size_t dim = 0; dim != data.numLoadDimensions(); ++dim)
    {
        loadAt[dim].erase(loadAt[dim].begin() + idx);
        loadBefore[dim].erase(loadBefore[dim].begin() + idx);
        loadAfter[dim].erase(loadAfter[dim].begin() + idx);
    }

    durAt.erase(durAt.begin() + idx);
    durBefore.erase(durBefore.begin() + idx);
    durAfter.erase(durAfter.begin() + idx);

#ifndef NDEBUG
    dirty = true;
#endif
}

void Route::swap(Node *first, Node *second)
{
    // TODO specialise std::swap for Node
    std::swap(first->route_->nodes[first->idx_],
              second->route_->nodes[second->idx_]);

    // Only need to swap the segments *at* the client's index. Other cached
    // values are recomputed based on these values, and that recompute will
    // overwrite the other outdated (cached) segments.
    std::swap(first->route_->distAt[first->idx_],
              second->route_->distAt[second->idx_]);
    std::swap(first->route_->durAt[first->idx_],
              second->route_->durAt[second->idx_]);

    for (size_t dim = 0; dim != first->route_->data.numLoadDimensions(); ++dim)
        std::swap(first->route_->loadAt[dim][first->idx_],
                  second->route_->loadAt[dim][second->idx_]);

    std::swap(first->route_, second->route_);
    std::swap(first->idx_, second->idx_);

#ifndef NDEBUG
    first->route_->dirty = true;
    second->route_->dirty = true;
#endif
}

void Route::update()
{
    centroid_ = {0, 0};

    for (size_t idx = 1; idx != nodes.size(); ++idx)
    {
        auto const *node = nodes[idx];
        size_t const client = node->client();

        if (!node->isDepot())
        {
            ProblemData::Client const &clientData = data.location(client);
            centroid_.first += static_cast<double>(clientData.x) / size();
            centroid_.second += static_cast<double>(clientData.y) / size();
        }
    }

    // Distance.
    for (size_t idx = 1; idx != nodes.size(); ++idx)
        distBefore[idx] = DistanceSegment::merge(
            data.distanceMatrix(profile()), distBefore[idx - 1], distAt[idx]);

    for (auto idx = nodes.size() - 1; idx != 0; --idx)
        distAfter[idx - 1] = DistanceSegment::merge(
            data.distanceMatrix(profile()), distAt[idx - 1], distAfter[idx]);

#ifndef PYVRP_NO_TIME_WINDOWS
    // Duration.
    for (size_t idx = 1; idx != nodes.size(); ++idx)
        durBefore[idx] = DurationSegment::merge(
            data.durationMatrix(profile()), durBefore[idx - 1], durAt[idx]);

    for (auto idx = nodes.size() - 1; idx != 0; --idx)
        durAfter[idx - 1] = DurationSegment::merge(
            data.durationMatrix(profile()), durAt[idx - 1], durAfter[idx]);
#endif

    // Load.
    for (size_t dim = 0; dim != data.numLoadDimensions(); ++dim)
    {
        for (size_t idx = 1; idx != nodes.size(); ++idx)
            loadBefore[dim][idx] = LoadSegment::merge(loadBefore[dim][idx - 1],
                                                      loadAt[dim][idx]);

        load_[dim] = loadBefore[dim].back().load();
        excessLoad_[dim] = std::max<Load>(load_[dim] - capacity()[dim], 0);

        for (auto idx = nodes.size() - 1; idx != 0; --idx)
            loadAfter[dim][idx - 1]
                = LoadSegment::merge(loadAt[dim][idx - 1], loadAfter[dim][idx]);
    }

#ifndef NDEBUG
    dirty = false;
#endif
}

std::ostream &operator<<(std::ostream &out, pyvrp::search::Route const &route)
{
    out << "Route #" << route.idx() + 1 << ":";  // route number
    for (auto *node : route)
        out << ' ' << node->client();  // client index
    out << '\n';

    return out;
}
